# robot.py
import numpy as np

class Node:
    def __init__(self, x, y, pinned=False):
        self.pos = np.array([float(x), float(y)])
        self.prev = self.pos.copy()
        self.vel = np.zeros(2)
        self.mass = 1.0
        self.pinned = pinned

class Link:
    def __init__(self, a: Node, b: Node, rest_length=None, link_type='rigid'):
        self.a = a
        self.b = b
        self.type = link_type  # 'rigid', 'prismatic', 'rotary'
        self.rest_length = rest_length if rest_length is not None else np.linalg.norm(a.pos - b.pos)
        self.stiffness = 1.0
        # actuator state
        self.actuator_target = self.rest_length
        self.actuator_speed = 0.0
        self.torque = 0.0

    def current_length(self):
        return np.linalg.norm(self.a.pos - self.b.pos)

class Robot:
    def __init__(self):
        self.nodes = []
        self.links = []

    def add_node(self, x, y, pinned=False):
        n = Node(x, y, pinned)
        self.nodes.append(n)
        return n

    def add_link(self, a, b, link_type='rigid'):
        l = Link(a, b, link_type=link_type)
        self.links.append(l)
        return l

    def state(self):
        # return simple serializable state
        nodes = [{'x': float(n.pos[0]), 'y': float(n.pos[1]), 'pinned': bool(n.pinned)} for n in self.nodes]
        links = [{'a': self.nodes.index(l.a), 'b': self.nodes.index(l.b), 'type': l.type, 'rest_length': float(l.rest_length)} for l in self.links]
        return {'nodes': nodes, 'links': links}
