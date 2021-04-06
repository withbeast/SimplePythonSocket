#### 简介

对python原生socket进行简单封装,不依赖第三方插件，能够实现发送和接收任意字节的数据，并且结合了python threading模块，使得服务端能够连接多个客户端。

#### 主要功能

* 接收和发送任意字节的数据。
* 内部使用threading模块，实现服务端多链接。
* 提供简单的服务器端用户列表。
* 只有一个文件 ，简单方便，能够灵活的嵌入到项目中。

#### 使用

将文件TcpSocket.py复制到项目中，通过import的方式使用简单封装的Socket

```python
from TcpSocket import tcp_socekt_server as server
from TcpSocket import tcp_socket_client as client
from TcpSocket import tcp_socket as sock
from TcpSocket import node
from TcpSocket import node_list as list
```

项目中的client.py和server.py是示例程序。下面对两个文件具体解析

client.py文件

```python
from TcpSocket import tcp_socket_client as client
from TcpSocket import tcp_socket as sock
##tcp_socket类型变量可以用来调用发送方法和接收方法

def on_connect(s: sock):##连接成功回调函数会接收一个tcp_socket类型的参数 函数可以用来处理与服务器的初始交互，比如注册名称等
    name = "king"
    s.send_struct(name)
    return


def recv_handler(s: sock):
    while True:
        msg = s.recv_struct() ## recv_struct 函数可以接收任意字节的而数据
        print(msg)


c = client("xxx.xxx.xxx.xxx", 16666) ##设置连接IP和端口
c.on_connect=on_connect ##设置连接成功回调函数
c.handler=recv_handler ##设置主处理函数
c.connect() ##连接
while True: ## 控制台输入
    s=input()
    c.sock.send_struct(s)
```

server.py文件

```python
from TcpSocket import tcp_socekt_server as server
from TcpSocket import tcp_socket as sock
from TcpSocket import node
from TcpSocket import node_list as list
from TcpSocket import log

def on_accept(s: sock):
    name=s.recv_struct()
    s.send_struct("连接成功")
    log(name+":连入")
    return True, name ##第一个布尔变量表示是否允许与当前客户端建立连接，第二个参数用于标识该客户端，并记录到用户列表list中。


def handler(n: node, l: list):
    while True:
        d = n.sock.recv_struct()
        if d==None:
            log("接收失败")
            break
        log("接收:"+d)
        msg = d + ":" + n.id
        n.sock.send_struct(msg)


s = server("0.0.0.0", 16666) #设置监听IP和端口
s.on_accept=on_accept #监听成功回调函数
s.handle=handler #监听主处理函数
s.listen(10) #设置最大连接量并开始监听
```

反馈邮箱：15838601879@163.com