# gui.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPen
NODE_R = 6

class PlaygroundWindow(QMainWindow):
    def __init__(self, sim):
        super().__init__()
        self.setWindowTitle('Robotics Playground')
        self.sim = sim
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints())
        self.view.setDragMode(QGraphicsView.NoDrag)

        # simple controls
        btn_start = QPushButton('Start Sim')
        btn_stop = QPushButton('Stop Sim')
        btn_step = QPushButton('Step')
        btn_state = QPushButton('Print State')

        btn_start.clicked.connect(self.sim.start)
        btn_stop.clicked.connect(self.sim.stop)
        btn_step.clicked.connect(self.step_once)
        btn_state.clicked.connect(self.print_state)

        topbar = QHBoxLayout()
        topbar.addWidget(btn_start)
        topbar.addWidget(btn_stop)
        topbar.addWidget(btn_step)
        topbar.addWidget(btn_state)

        container = QWidget()
        layout = QVBoxLayout()
        layout.addLayout(topbar)
        layout.addWidget(self.view)
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.node_items = []
        self.link_items = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.sync_view)
        self.timer.start(30)

        # enable simple interaction: double click to create node
        self.view.viewport().installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == event.MouseButtonDblClick:
            pos = self.view.mapToScene(event.pos())
            with self.sim.lock:
                self.sim.add_node(pos.x(), pos.y(), pinned=False)
            return True
        return super().eventFilter(obj, event)

    def step_once(self):
        self.sim.step()
        self.sync_view()

    def print_state(self):
        print(self.sim.get_state())

    def sync_view(self):
        # clear and redraw (simple approach)
        self.scene.clear()
        with self.sim.lock:
            for l in self.sim.robot.links:
                a = l.a.pos
                b = l.b.pos
                line = QGraphicsLineItem(a[0], a[1], b[0], b[1])
                pen = QPen(Qt.black)
                pen.setWidth(2)
                line.setPen(pen)
                self.scene.addItem(line)
            for n in self.sim.robot.nodes:
                x, y = n.pos
                circ = QGraphicsEllipseItem(x - NODE_R, y - NODE_R, NODE_R * 2, NODE_R * 2)
                circ.setBrush(Qt.gray)
                self.scene.addItem(circ)
