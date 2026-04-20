# BlendAgent-MCP
🛠 Project Overview
BlendAgent-MCP is a cutting-edge implementation of the Model Context Protocol (MCP), designed to turn Large Language Models (like Claude 3.5 Sonnet and GPT Models) into expert 3D artists. By exposing Blender’s powerful BPY (Blender Python API) to AI agents, this project enables a seamless "Text-to-3D-Action" workflow.

Instead of navigating complex menus, users can simply describe their scene, and the AI agent executes the necessary Python scripts in real-time within Blender.

✨ Key Features
Natural Language Modeling: Create primitives, modify meshes, and arrange scenes using simple English commands.

Smart Rendering Pipeline: Automate camera setups, focal length adjustments, and render engine configurations (Cycles/Eevee).

Procedural Lighting: Dynamic placement of Point, Sun, and Area lights based on the desired mood of the scene.

Material Automation: Assign and tweak shaders and textures via AI without touching the Shader Editor.

Context-Aware Execution: The MCP server ensures the AI understands the current state of the Blender scene before suggesting changes.

🚀 Why This Matters (The "Wow" Factor)
In a traditional 3D pipeline, repetitive tasks like setting up environment lighting or cleaning up a scene can take hours. BlendAgent-MCP reduces this to seconds.

For Artists: Focus on creativity while the AI handles the "grunt work."

For Developers: Build 3D environments programmatically without deep knowledge of the BPY API.

Technopreneurship Goal: This project is a prototype for a B2B SaaS tool aimed at game studios and architectural visualization firms to optimize their production speed.

🏗 Technical Stack
Protocol: Model Context Protocol (MCP)

Language: Python

API: Blender Python API (BPY)
