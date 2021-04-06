from TcpSocket import tcp_socekt_server as server
from TcpSocket import tcp_socket as sock
from TcpSocket import node
from TcpSocket import node_list as list
from TcpSocket import log

def on_accept(s: sock):
    name=s.recv_struct()
    s.send_struct("连接成功")
    log(name+":连入")
    return True, name


def handler(n: node, l: list):
    while True:
        d = n.sock.recv_struct()
        if d==None:
            log("接收失败")
            break
        log("接收:"+d)
        msg = d + ":" + n.id
        n.sock.send_struct(msg)


s = server("0.0.0.0", 16666)
s.on_accept=on_accept
s.handle=handler
s.listen(10)
