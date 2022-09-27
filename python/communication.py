import threading as th
import socket
from main import stream

class Communication:

    def __init__(self, host, src_port, dst_ip, dst_port):
        self.send_th = th.Thread(target=lambda: self.send_stream(dst_ip, dst_port))
        self.recv_th = th.Thread(target=lambda: self.receive_stream(host, src_port))
        self.lock = th.Lock()
    
    def start(self):
        self.recv_th.start()
        self.send_th.start()
    
    def is_alive(self):
        return self.recv_th.is_alive()

    def receive_stream(self, UDP_IP, UDP_PORT):
        sock = socket.socket(socket.AF_INET, # Internet
                            socket.SOCK_DGRAM) # UDP
        sock.settimeout(5)
        sock.bind((UDP_IP, UDP_PORT))
        print('waiting for video...')
        try:
            while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                if self.lock.locked():
                    return
                data = data.decode('utf-8')
                if data == ">>>":
                    buffer = ""
                    while True:
                        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                        data = data.decode('utf-8')
                        if data == "<<<":
                            break
                        buffer += data
                    print(buffer)
        except socket.timeout:
            print('timeout, stop communication...')
        finally:
            self.lock.acquire()
            sock.close()

    def send(self, buffer, sock, UDP_IP, UDP_PORT):
        if self.lock.locked():
            return "STOP"
        size = len(buffer)
        i = 0
        MAX = 1023
        sock.sendto(">>>".encode('utf-8'), (UDP_IP, UDP_PORT))
        while size >= MAX:
            sock.sendto(buffer[i:i+MAX-2].encode('utf-8'), (UDP_IP, UDP_PORT))
            i += MAX-2
            size -= MAX-2
        if size > 0:
            sock.sendto(buffer[i::].encode('utf-8'), (UDP_IP, UDP_PORT))
        sock.sendto("<<<".encode('utf-8'), (UDP_IP, UDP_PORT))

    def send_stream(self, UDP_IP, UDP_PORT):
        print("sending video...")
        sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
        stream(lambda buffer: self.send(buffer, sock, UDP_IP, UDP_PORT))