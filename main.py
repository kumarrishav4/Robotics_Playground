# main.py
import sys
from PySide6.QtWidgets import QApplication
from gui import PlaygroundWindow
from network import CommandServer
from simulator import Simulator

PORT = 20000

if __name__ == '__main__':
    app = QApplication(sys.argv)

    sim = Simulator(dt=0.016)
    win = PlaygroundWindow(sim)
    win.resize(1100, 700)
    win.show()

    # start TCP server (runs in background thread)
    server = CommandServer(sim, host='0.0.0.0', port=PORT)
    server.start()

    sys.exit(app.exec())
