# simulator.py
import time
import threading
import numpy as np
from robot import Robot

class Simulator:
    def __init__(self, dt=0.016):
        self.robot = Robot()
        self.dt = dt
        self.running = False
        self.lock = threading.RLock()
        self.gravity = np.array([0.0, 0.0])
        self.damping = 0.98

    def step(self):
        with self.lock:
            # simple verlet-like integrator
            for n in self.robot.nodes:
                if n.pinned:
                    n.prev = n.pos.copy()
                    n.vel[:] = 0
                    continue
                temp = n.pos.copy()
                n.vel = (n.pos - n.prev) / (self.dt + 1e-12)
                n.vel = n.vel * self.damping + self.gravity * self.dt
                n.pos = n.pos + n.vel * self.dt
                n.prev = temp

            # constraints: resolve links
            for _ in range(4):
                for l in self.robot.links:
                    a, b = l.a, l.b
                    delta = b.pos - a.pos
                    cur_len = np.linalg.norm(delta)
                    if cur_len == 0:
                        continue
                    # actuator desired length
                    if l.type == 'prismatic':
                        target = l.actuator_target
                    else:
                        target = l.rest_length

                    diff = (cur_len - target) / cur_len
                    # distribute correction by mass (equal here)
                    if not a.pinned and not b.pinned:
                        a.pos += 0.5 * diff * delta
                        b.pos -= 0.5 * diff * delta
                    elif a.pinned and not b.pinned:
                        b.pos -= diff * delta
                    elif b.pinned and not a.pinned:
                        a.pos += diff * delta

    def run(self):
        self.running = True
        while self.running:
            t0 = time.time()
            self.step()
            elapsed = time.time() - t0
            sleep = max(0, self.dt - elapsed)
            time.sleep(sleep)

    def start(self):
        if hasattr(self, 'thread') and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=0.2)

    # convenience wrappers for external control
    def get_state(self):
        with self.lock:
            return self.robot.state()

    def add_node(self, x, y, pinned=False):
        with self.lock:
            return self.robot.add_node(x, y, pinned)

    def add_link(self, a_idx, b_idx, link_type='rigid'):
        with self.lock:
            a = self.robot.nodes[a_idx]
            b = self.robot.nodes[b_idx]
            return self.robot.add_link(a, b, link_type)
