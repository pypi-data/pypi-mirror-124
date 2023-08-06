import socket
from dataclasses import dataclass

@dataclass
class CherrySocketWrapper:

    CHERRY_PORT = 10019
    CHUNK_MAX_SIZE = 65536

    def __init__(self, ip):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((ip,CherrySocketWrapper.CHERRY_PORT))
        self.socket.setblocking(False)

    def read_available_bytes(self):
        buffer_end = False
        buffer = b''
        while not buffer_end:
            try:
                chunk = self.socket.recv(CherrySocketWrapper.CHUNK_MAX_SIZE)
                buffer += chunk
                if chunk.__len__() < CherrySocketWrapper.CHUNK_MAX_SIZE:
                    buffer_end = True
            except BlockingIOError:
                buffer_end = True
        return buffer

    def write(self, byte_array):
        self.socket.send(byte_array)

    def close(self):
        self.socket.close()

