from bffacilities.utils import createLogger
logger = createLogger('network', savefile=False, stream=True, timeformat="%H:%M:%S")
import socket
if hasattr(socket, "epoll"):
    from .servers import TcpSocketServer, SocketClient, UdpSocketClient, UdpSocketServer
else:
    from .socketserver_select import TcpSocketServer, SocketClient, UdpSocketClient, UdpSocketServer