# network.py
import socket
import threading
import json

class CommandServer(threading.Thread):
    def __init__(self, simulator, host='0.0.0.0', port=20000):
        super().__init__(daemon=True)
        self.sim = simulator
        self.host = host
        self.port = port
        self.sock = None
        self.clients = []

    def handle_client(self, conn, addr):
        with conn:
            buff = b''
            while True:
                try:
                    data = conn.recv(4096)
                except ConnectionResetError:
                    break
                if not data:
                    break
                buff += data
                # allow multiple JSON messages separated by newline
                while b"\n" in buff:
                    line, buff = buff.split(b"\n", 1)
                    try:
                        cmd = json.loads(line.decode('utf8'))
                    except Exception as e:
                        conn.send(b'{"error":"bad json"}\n')
                        continue
                    resp = self.process(cmd)
                    conn.send((json.dumps(resp) + "\n").encode('utf8'))

    def process(self, cmd):
        # simple dispatch
        try:
            if cmd.get('cmd') == 'get_state':
                return {'status': 'ok', 'state': self.sim.get_state()}
            if cmd.get('cmd') == 'add_node':
                n = self.sim.add_node(cmd['x'], cmd['y'], cmd.get('pinned', False))
                return {'status': 'ok', 'idx': self.sim.robot.nodes.index(n)}
            if cmd.get('cmd') == 'add_link':
                _ = self.sim.add_link(cmd['a'], cmd['b'], cmd.get('type', 'rigid'))
                return {'status': 'ok'}
            if cmd.get('cmd') == 'set_prismatic':
                li = self.sim.robot.links[cmd['idx']]
                if li.type != 'prismatic':
                    return {'status': 'error', 'msg': 'link not prismatic'}
                li.actuator_target = float(cmd['target'])
                return {'status': 'ok'}
            if cmd.get('cmd') == 'start_sim':
                self.sim.start()
                return {'status': 'ok'}
            if cmd.get('cmd') == 'stop_sim':
                self.sim.stop()
                return {'status': 'ok'}
            return {'status': 'error', 'msg': 'unknown command'}
        except Exception as e:
            return {'status': 'error', 'msg': str(e)}

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(4)
        while True:
            conn, addr = self.sock.accept()
            t = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
            t.start()
