Absolutely! Here’s a **professional, detailed, and clear README** for your robotics simulator project. You can save this as `README.md` in your project root.

````markdown
# Robotics Simulator Playground

A Python-based **interactive robotics simulator** with a GUI playground for designing, testing, and controlling robotic linkages. Supports **nodes, prismatic joints, rotary actuators**, and external control via **Python or MATLAB clients** over TCP sockets.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [GUI Overview](#gui-overview)
- [Simulator API](#simulator-api)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Drag-and-drop nodes** to create joints.
- **Prismatic joints** (linear actuators) connecting nodes.
- **Rotary actuators** for rotational motion.
- **Interactive GUI** using PySide6.
- **TCP socket communication**:
  - Python client
  - MATLAB client
- **Live simulation** with step updates.
- **JSON-based API** for easy integration.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Robotics_Simulator.git
cd Robotics_Simulator
````

2. Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows PowerShell
# or source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
.\run.bat
```

---

## Usage

* Launch the GUI using `run.bat`.
* Drag nodes onto the canvas to create joints.
* Right-click a node or link to convert to a **rotary actuator**.
* Connect to the simulator using the TCP API for automated control.

---

## GUI Overview

* **Canvas**: Main area to place and connect nodes.
* **Node**: Represents a joint point. Can be dragged.
* **Link**: Connects two nodes, can be prismatic or rotary.
* **Toolbar**:

  * Add Node
  * Add Link
  * Delete Node/Link
  * Start/Stop Simulation

---

## Simulator API

**TCP Commands** (JSON-based):

* **Add Node**

```json
{"cmd": "add_node", "x": 100, "y": 200}
```

* **Add Link**

```json
{"cmd": "add_link", "node_a": 1, "node_b": 2, "type": "prismatic"}
```

* **Set Rotary Target**

```json
{"cmd": "set_rotary", "id": 2, "target": 1.57}
```

* **Get Status**

```json
{"cmd": "get_status"}
```

**Response Example:**

```json
{
  "nodes": [{"id": 1, "x": 100, "y": 200}],
  "links": [{"id": 2, "type": "rotary", "theta": 0.0, "theta_target": 1.57}]
}
```

---

## Examples

* **Python client**: `examples/client_python.py`
* **MATLAB client**: `examples/client_matlab.m`

These scripts demonstrate connecting to the simulator, adding nodes/links, and moving actuators programmatically.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## License



