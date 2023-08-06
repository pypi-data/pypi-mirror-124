'''
 # @ Author: brifuture
 # @ Create Time: 2021-04-15 12:16
 # @ Modified by: brifuture
 # @ Modified time: 2021-06-11 12:01
 # @ Description: This File is created and the program is coded by BriFuture. (c) All rights reserved.
    Provides TCP/UDP socket Server and client
 '''

import json
import socket
import select
import traceback
import logging
logger = logging.getLogger("network")

__version__ = "0.2.0"

class EventHandler:
    def fileno(self):
        """Return the associated file descriptor"""
        raise ValueError('Not Implemented must implement')

    def handle_receive(self):
        'Perform the receive operation'
        pass

    def handle_send(self):
        'Send outgoing data'
        pass

    def handle_except(self):
        pass

    def is_valid(self):
        return True

class SocketClient(EventHandler):
    """
    1. 通过继承该类进行客户端编写，
    2. 通过 parser 回调函数进行消息读取

    Args:
        sock: socket
        address: client socket address recved from server,
            useful when other want to communicate or 
            identify the client

        except_callback: function(client: SocketClient)
    """
    def __init__(self, sock, address, **kwargs):
        self._sock = sock
        self._sock.setblocking(False)
        if address is None:
            try:
                self.address = self._sock.getsockname()
            except: 
                self.address = None
        else:
            self.address = address

        self._isValid = True

        self._parse = None
        self._server = None
        self.except_callback = kwargs.get("except_callback", None)
        self.bufferSize = kwargs.get("bufferSize", 2048)

    @staticmethod
    def createTcpClient(serverAddr):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sc = SocketClient(sock, None)
        sc._sock.setblocking(True)
        sc._server = serverAddr
        return sc

    @property
    def sock(self):
        return self._sock

    def connect(self):
        if self._server is None:
            return
        try:
            self._sock.connect(self._server)
            if self.address is None:
                self.address = self._sock.getsockname()
        except:
            logger.warning(f"[SC] Error connecting {self._server} [{self.address}]")
            self.handle_except()
        finally:
            pass

    def shutdown(self):
        self._sock.close()

    def __del__(self):
        self._sock.close()

    @property
    def parser(self):
        return self._parse

    @parser.setter
    def parser(self, parse):
        """传入一个解析器即可
        @deprecated use setParser
        ```py
        # data is a dict
        def parse(data, socketClient): print(data, socketClient)

        client.parser = parse
        ```
        """
        try:
            parse('""', self) # pass empty string
            self._parse = parse
        except:
            logger.critical(f"[TC] ***** Error testing parser, it will be ignored ****")

    def setParser(self, parser, testJson=True):
        if testJson:
            try:
                parser('""', self) # pass empty string
                self._parse = parser
            except:
                logger.critical(f"[TC] ***** Error testing parser, it will be ignored ****")
        else:
            self._parse = parser

    def is_valid(self):
        return self._isValid

    def fileno(self):
        return self._sock.fileno()

    def __repr__(self):
        return f'<SockClient, {self._sock.fileno()}, {self.address}>'

    def handle_receive(self):
        """Handle receive data, default processor
        subclass could replace this methods to receive binary data
        """
        msg = None
        try:
            msg = self._sock.recv(self.bufferSize)
            if not msg:
                self.handle_except()
                return
        except socket.error:
            self.handle_except()
        except Exception as e:
            logger.warning(f"[TC] recv {e}")
        
        if msg is None: return

        if self._parse:
            try:
                self._parse(msg.decode(), self)
            except Exception as e:
                logger.warning(f"[TC] parse {msg}, {e}")
                traceback.print_exc()
        else:
            logger.debug(msg)

    def handle_send(self):
        pass

    def handle_except(self):
        """注意不要在 callback 中重新创建 client，否则函数调用堆栈将会溢出
        """
        self._sock.close()
        self._isValid = False
        if self.except_callback:
            self.except_callback(self)

import sys

class BaseServer():
    """ One can easily extend the base server for Tcp/Udp connection
    """
    maxsize = 500000
    def __init__(self):
        self._recvList = []
        self._sendList = []
        self._exceptList = []
        self.running = False
        try:
            self.epoll = select.epoll(self.maxsize)
        except:
            pass
    
    def __del__(self):
        try:
            self.epoll.close()
        except: 
            pass

    def stop(self):
        self.running = False

    def registerRead(self, r):
        if r in self._recvList:
            logger.debug(f"Client Registered Twice {r}")
            return
        logger.debug(f"Client Registered {r}")
        self.epoll.register(r.fileno(), select.EPOLLIN)
        self._recvList.append(r)

    def registerWrite(self, w):
        if w in self._sendList:
            return
        self.epoll.register(w.fileno(), select.EPOLLOUT)
        self._sendList.append(w)

    def serve_forever(self):
        self.running = True
        while self.running:
            self.serve_once(0.1)

    def serve_once(self, timeout=0.001):
        if len(self._recvList) == 0:
            return
        events = self.epoll.poll(timeout)

        for fileno, event in events:
            if event & select.EPOLLIN:
                for r in self._recvList:
                    if fileno == r.fileno():
                        r.handle_receive()
            elif event & select.EPOLLOUT:
                for s in self._sendList:
                    if fileno == s.fileno():
                        s.handle_send()
            elif event & select.EPOLLHUP:
                self.epoll.unregister(fileno)
                for r in self._recvList:
                    if fileno == r.fileno():
                        r.handle_except()
        # self.checkClients() # upper level call it

class TcpSocketServer(EventHandler, BaseServer):
    """
    Args:
        ip address
        port
    """
    ClientClass = SocketClient
    def __init__(self, ip, port, maxconn = 100000):
        super().__init__()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._clients = {}
        # key: address tuple, value SocketClient
        self.registerRead(self)
        
        self._exceptList.append(self)
        self._clientAdded = None
        self._clientRemoved = None
        try:
            self._server.bind((ip, port))
            logger.info(f"[TSS] Server Listening: {ip}:{port}")
        except Exception as e:
            logger.critical(f"[TS] Unable to listening {ip}:{port}")
            sys.exit(1)

        self._server.listen(maxconn)
        self._server.setblocking(False)
        self.maxconn = maxconn

    def setClientAddedCallback(self, p):
        """ callback """
        self._clientAdded = p

    def setClientRemovedCallback(self, p):
        """ callback """
        self._clientRemoved = p

    def fileno(self):
        return self._server.fileno()

    def __repr__(self) -> str:
        return f"<TSS {self.fileno()} c: {len(self._recvList)}>"

    def needs_receive(self):
        return True

    def serve_forever(self):
        self.running = True
        count = 0
        while self.running:
            self.serve_once(0.01)
            count += 1
            if count % 12000 == 0:
                self.checkClients()

    def shutdown(self):
        self.removeAll()
        self._server.close()

    def __del__(self):
        self.shutdown()

    def checkClients(self):
        clients = list(self._clients.values())
        for c in clients:
            if not c.is_valid():
                self.removeClient(c)
        # logger.debug(f"Check Clients {len(self._clients)}")

    def removeAll(self):
        clients = list(self._clients.values())
        for c in clients:
            c.shutdown()
            self.removeClient(c)

    def removeClient(self, client):
        """
        Args
            client: SocketClient
        """
        if client == self: return

        logger.info(f"[TS] Removing {client.address} {len(self._recvList)}")
        if client in self._recvList:
            try:
                self._recvList.remove(client)
            except: pass
        if client in self._exceptList:
            try:
                self._exceptList.remove(client)
            except: pass
            
        if client.address in self._clients:
            try:
                self._clients.pop(client.address, None)
            except: pass
            
        if self._clientRemoved:
            try:
                self._clientRemoved(client)
            except Exception as e:
                logger.warning(f"[TS] remove callback failed {e}")
    
    def _addClient(self, sock, address):
        """添加一个 客户端 socket，不可手动添加
        """

        c = TcpSocketServer.ClientClass(sock, address, except_callback=self.removeClient)
        self._clients[address] = (c)
        # self._recvList.append(c)
        self._exceptList.append(c)
        self.registerRead(c)
        if self._clientAdded:
            self._clientAdded(c)

    def handle_receive(self):
        """接收到TCP连接
        """
        (sock, address) = self._server.accept()
        if len(self._clients) >= self.maxconn:
            # 超出最大连接数
            logger.warning("[TSS] Receive many conns")
            sock.close()
            return
        if address not in self._clients:
            self._addClient(sock, address)
            logger.debug(f'[TS] Accept From {address}, Clients Count: {len(self._clients)}')
        else:
            self._clients[address].sock = sock
            self._clients[address].address = address
            self._clients[address]._isValid = True

from datetime import datetime
import threading

class UdpSocketClient(EventHandler):
    def __init__(self, port, ip = "127.0.0.1", name="default", **kwargs):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (ip, port)
        self.sock.settimeout(0)
        self.sock.setblocking(False)
        self.sock.bind(self.address)
        self.bufferSize = kwargs.get("bufferSize", 1024)
        self.name = name
        self._isValid = True
        self._parse = None
        self._peer = None
        self._peers = []

        self.except_callback = kwargs.get("except_callback", None)
        # self.keepFirstPeer = False # if true, the first peer will always be used

    @property
    def parser(self):
        return self._parse

    @parser.setter
    def parser(self, parse):
        """传入一个解析器即可
        ```
        def parse(data, recver): 
            print(data, "From", recver)

        client.parser = parse
        ```
        """
        self._parse = parse

    def send(self, msg):
        """
        Args
            msg bytes
        """
        for p in self._peers:
            self.sock.sendto(msg, p)

    def is_valid(self):
        return self._isValid

    def fileno(self):
        return self.sock.fileno()

    def __repr__(self):
        return f"<UdpSocketClient {self.name} {self.address} {self.bufferSize} {self.sock.fileno()}>"

    def handle_receive(self):
        """Handle receive data, default processor
        subclass could replace this methods to receive binary data
        """
        bytesAddressPair = None
        try:
            bytesAddressPair = self.sock.recvfrom(self.bufferSize)
        except Exception as e: 
            # logger.warning(f"[UC] {self}  recv error : {e}")
            # traceback.print_exc()
            # ICMP recved cause the error, ignore it
            pass

        # message = bytesAddressPair[0]
        if not bytesAddressPair:
            # self.handle_except()
            return
        if not bytesAddressPair[1] in self._peers:
            logger.info(f"[UC] new client added: {bytesAddressPair[1]}")
            self._peers.append(bytesAddressPair[1])
        if self._parse:
            try: 
                self._parse(bytesAddressPair, self.name)
            except Exception as e:
                logger.warning(f"[UC] parse error: {e}")
                traceback.print_exc()

    def handle_send(self):
        pass

    def handle_except(self):
        self.sock.close()
        self._isValid = False
        if self.except_callback:
            self.except_callback(self)


class UdpSocketServer(BaseServer):
    """支持绑定到多个UDP端口上，使用 processor 进行回调

    Args:
        port udpsocket will bind into

    Callback:
        processor(msg: bytes, addr: tuple)

    Usage:

    ```py
    server = UdpSocketServer(bufferSize = 4096)
    
    server.createListener(10000, "server1")
    server.addProcessor(lambda x, y: print(x, y), name="server1")

    # send 
    server.sendto("server1", b"this is a test")
    server.broadcast(b"this is a broadcast")

    # in default loop
    server.serve_forever()

    # in custom loop
    while True:
        ## .. do other things
        server.serve_once()
        ## .. do other things
    ```

    """
    ClientClass = UdpSocketClient
    def __init__(self, **kwargs):
        super().__init__()
        self._listeners = {}
        self.bufferSize = kwargs.get("bufferSize", 1024)
        self._processors = {}

    @property
    def listeners(self):
        return self._listeners

    def addProcessor(self, processor, name="default"):
        if name not in self._processors:
            self._processors[name] = processor
            # logger.debug(f"[USS] add processor for {name}")
        else:
            logger.warning("[USS] dumplicated add processor.")

    def createListener(self, port, name="default", ip="127.0.0.1", processor = None):
        if name in self._listeners.keys():
            return

        assert port > 0 and port < 65535, "In valid Port"

        logger.info(f"[USS] Server Listening for '{name}': {ip}:{port}")
        listener = self.ClientClass(port, ip, bufferSize=self.bufferSize, name=name)
        listener.parser = self.recvfrom
        listener.except_callback = self.handle_except

        self._listeners[name] = listener
        self._recvList.append(listener)
        self._exceptList.append(listener)
        if processor is not None:
            self.addProcessor(processor, name)
        # self._sendList.append(listener)
        return listener
    
    def handle_except(self, client):
        logger.warning(f"[USS] Listener quit, {client.name}")
        self._listeners.pop(client.name)
        self._recvList.remove(client)
        self._exceptList.remove(client)

    def send(self, msg: bytes, name = "default"):
        """send msg to server by
        """
        if name not in self._listeners:
            return
        self._listeners[name].send(msg)

    def sendto(self, msg: bytes, peer, name="default"):
        if name not in self._listeners:
            return
        self._listeners[name].sock.sendto(msg, peer)

    def broadcast(self, msg):
        for c in self._listeners.values():
            c.send(msg)

    def recvfrom(self, byteAddrPair, name):
        """recv data from one udp server
        """
        if name in self._processors:
            # process will executed
            process = self._processors[name]
            message = byteAddrPair[0]
            address = byteAddrPair[1]
            process(message, address)
        else:
            logger.debug(f"No processor for{name}, {byteAddrPair}")
