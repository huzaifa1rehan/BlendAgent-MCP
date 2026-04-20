from flask import Flask, render_template, request, jsonify
import openai
import socket
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=API_KEY)

def optimize_prompt(user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=300,
        messages=[
            {
                "role": "system",
                "content": """You are a Blender prompt optimizer. 
                Take the user prompt and rewrite it to be very specific for Blender Python bpy code generation.
                Add specifics like material settings, lighting, camera position.
                Return ONLY the optimized prompt, nothing else."""
            },
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_code(optimized_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=2000,
        messages=[
            {
                "role": "system",
                "content": """You are a Blender expert. Write only bpy Python code. 
                No markdown, no backticks, no explanation. Just raw Python code.
                When applying materials always use this exact method: 
                create new material with bpy.data.materials.new(), set use_nodes=True, 
                then access material.node_tree.nodes["Principled BSDF"] and set inputs 
                like Base Color, Roughness, Metallic directly. 
                Always clear existing materials first with obj.data.materials.clear() 
                before appending new material. 
                Always select object first with bpy.context.view_layer.objects.active = obj 
                before material operations.
                Do not use fcurves directly. For animation use keyframe_insert method only.
                Use math.sin and math.cos for circular animations."""
            },
            {"role": "user", "content": optimized_prompt}
        ]
    )
    return response.choices[0].message.content.strip()

def send_to_blender(code):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        sock.settimeout(15)

        command = {
            "type": "execute_code",
            "params": {"code": code}
        }

        sock.sendall(json.dumps(command).encode('utf-8'))

        response_data = b''
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response_data += chunk
                json.loads(response_data.decode('utf-8'))
                break
            except json.JSONDecodeError:
                continue

        sock.close()
        result = json.loads(response_data.decode('utf-8'))
        return result.get('status') == 'success', result.get('message', '')

    except Exception as e:
        return False, str(e)

history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    data = request.json
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify({'error': 'Prompt khali hai!'})

    start = datetime.now()

    try:
        # Step 1: Optimize
        optimized = optimize_prompt(prompt)

        # Step 2: Generate Code
        code = generate_code(optimized)

        # Step 3: Send to Blender
        success, msg = send_to_blender(code)

        elapsed = round((datetime.now() - start).total_seconds(), 1)
        status = 'success' if success else 'error'

        history.insert(0, {
            'prompt': prompt,
            'status': status,
            'time': datetime.now().strftime('%H:%M:%S'),
            'elapsed': elapsed
        })

        return jsonify({
            'optimized': optimized,
            'code': code,
            'success': success,
            'elapsed': elapsed,
            'message': msg
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/history')
def get_history():
    return jsonify(history[:20])

if __name__ == '__main__':
    app.run(debug=True, port=5000)