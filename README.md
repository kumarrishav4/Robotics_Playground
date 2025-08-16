# Robotics Playground

Minimal 2D robotics playground with PySide6 GUI and a JSON-over-TCP command server.

## Quick start (Windows)
1. Install Python 3.10+
2. Open a command prompt in this folder
3. pip install -r requirements.txt
4. python main.py
5. Double-click on the canvas to add nodes. Use the TCP API to add links or control actuators.

## TCP protocol (newline-delimited JSON)
- {'cmd':'get_state'}
- {'cmd':'add_node','x':..,'y':..}
- {'cmd':'add_link','a':index,'b':index,'type':'prismatic'|'rigid'}
- {'cmd':'set_prismatic','idx':link_index,'target':length}
- {'cmd':'start_sim'}
- {'cmd':'stop_sim'}
