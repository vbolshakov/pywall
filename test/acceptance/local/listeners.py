from datetime import datetime
from datetime import timedelta


class BaseListener(object):
    """
    Base class for listeners. Extend and implement listen() to suit
    your acceptance test.
    """
    __metaclass__ = ABCMeta
    def __init__(self, msg='knock-knock'):
        self._msg = msg

    @abstractmethod
    def listen(self, queue, sem):
        """Puts True in queue if it gets message on socket, False otherwise"""
        pass


class TCPListener(BaseListener):
    def __init__(self, host, port, msg='knock-knock', timeout=5):
        BaseListener.__init__(self, msg=msg)
        self._port = port
        self._remote_host_ip = socket.gethostbyname(host)
        self._timeout = 5

    def listen(self, queue, sem):
        print('listening')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0', self._port))
        sock.listen(5)
        sock.settimeout(self._timeout)
        sem.release()

        start = datetime.now()
        print('before loop')
        try:
            while start + timedelta(seconds=self._timeout) < datetime.now():
                s, (host_ip, host_port) = sock.accept()
                if host_ip == self._remote_host_ip:
                    msg = s.recv(1024)
                    print(msg)
                    queue.put(msg == self._msg)
                    s.close()
                    break
                s.close()
            sock.close()
        except socket.timeout:
            sock.close()
            queue.put(False)
        print('done listening')


class UDPListener(BaseListener):
    def __init__(self, host, port, msg='knock-knock', timeout=5):
        BaseListener.__init__(self, msg=msg)
        self._port = port
        self._remote_host_ip = socket.gethostbyname(host)
        self._timeout = 5

    def listen(self, queue, sem):
        print('listening')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', self._port))
        sock.listen(5)
        sock.settimeout(self._timeout)
        sem.release()

        start = datetime.now()
        print('before loop')
        try:
            while start + timedelta(seconds=self._timeout) < datetime.now():
                s, (host_ip, host_port) = sock.accept()
                if host_ip == self._remote_host_ip:
                    msg = s.recv(1024)
                    print(msg)
                    queue.put(msg == self._msg)
                    s.close()
                    break
                s.close()
            sock.close()
        except socket.timeout:
            sock.close()
            queue.put(False)
        print('done listening')