from TcpSocket import tcp_socket_client as client
from TcpSocket import tcp_socket as sock


def on_connect(s: sock):
    name = "king"
    s.send_struct(name)
    return


def recv_handler(s: sock):
    while True:
        msg = s.recv_struct()
        print(msg)


c = client("49.235.220.45", 16666)
c.on_connect=on_connect
c.handler=recv_handler
c.connect()
while True:
    s=input()
    c.sock.send_struct(s)
