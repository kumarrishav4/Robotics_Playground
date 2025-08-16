# examples/py_client.py
import socket, json

def send(cmd, host='127.0.0.1', port=20000):
    s = socket.create_connection((host, port), timeout=2)
    s.send((json.dumps(cmd) + "\n").encode('utf8'))
    resp = s.recv(65536)
    s.close()
    return json.loads(resp.decode('utf8'))

if __name__ == '__main__':
    print(send({'cmd':'start_sim'}))
    print(send({'cmd':'add_node','x':100,'y':100}))
    print(send({'cmd':'add_node','x':200,'y':100}))
    print(send({'cmd':'add_link','a':0,'b':1,'type':'prismatic'}))
    print(send({'cmd':'get_state'}))
