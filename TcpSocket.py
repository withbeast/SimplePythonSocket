import struct
from threading import Thread
import socket
import json


def log(obj):
    f = open("log.txt", "a")
    print(obj, file=f)
    f.close()


class tcp_socket():
    _sock: socket.socket = None
    code: str = "utf-8"
    _pack_len = 1024

    def __init__(self, sock: socket.socket):
        self._sock = sock

    def send_struct(self, msg: str):# 发送任意大小的数据
        c = msg.encode(self.code)
        b = struct.pack('>I', len(c)) + c
        self._sock.sendall(b)

    def recv_struct(self):# 接收任意大小的数据
        raw = self._sock.recv(4)
        if not raw:
            return None
        msg_len = struct.unpack('>I', raw)[0]
        d = b''
        while len(d) < msg_len:
            packet = self._sock.recv(msg_len - len(d))
            if not packet: return None
            d += packet
        if d != None: return d.decode(self.code)
        return None

    def send(self, msg: str):# 简单发送
        self._sock.send(msg.encode(self.code))

    def recv(self):# 简单接收
        d=self._sock.recv(1024)
        return d.decode(self.code)



class node:
    sock = None
    id = None

    def __init__(self, sock: tcp_socket, id):
        self.sock = sock
        self.id = id


class node_list():
    _list: [node] = None

    def __init__(self, list: [node]):
        self._list = list

    def get_sock(self, id) -> tcp_socket:
        for n in self._list:
            if n.id == id:
                return n.sock


class tcp_socekt_server():
    _server_sock = None
    _nodeList = [] #连接列表
    host = "0.0.0.0"
    port = 0
    on_accept_func = None #监听接收函数
    handler = None #数据接收函数
    code = "utf-8"

    def __init__(self, host="0.0.0.0", port=0):
        self.host = host
        self.port = port

    def listen(self, backlog=10):
        self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_sock.bind((self.host, self.port))
        self._server_sock.listen(backlog)
        while True:
            s, address = self._server_sock.accept()
            sock = tcp_socket(s)
            canConnect, id = self.on_accept_func(sock)
            n = node(sock, id)
            self._nodeList.append(n)
            if canConnect:
                thread = Thread(target=self._self_handler, args=(n, self._nodeList))
                thread.setDaemon(True)
                thread.start()

    def _self_handler(self, node,list):
        self.handler(node,list)
        self._nodeList.remove(node)

    def notify_all(self, str):
        for node in self._nodeList:
            node.sock.sendall(str.encode(self.code))

    def get_sock(self, id):
        for node in self._nodeList:
            if node.id == id:
                return node.sock
        return None

    def close(self):
        self._server_sock.close()


class tcp_socket_client():
    _client_sock = None
    sock = None
    _host = ""
    _port = 0
    on_connect = None 
    handler = None #接收函数
    code = "utf-8"

    def __init__(self, host, port):
        self._host = host
        self._port = port

    def connect(self):
        self._client_sock = socket.socket()  # 创建 socket 对象
        self._client_sock.connect((self._host, self._port))
        self.sock = tcp_socket(self._client_sock)
        self.on_connect(self.sock)
        t1 = Thread(target=self.handler, args=(self.sock,), name="接收线程")  # 设置接收线程
        t1.setDaemon(True)  # 开启守护线程模式
        t1.start()

