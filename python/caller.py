from sender import send_stream
from receiver import receive_stream
import threading as th
from register import get_contact
from communication import Communication
import socket, errno

IP = socket.gethostbyname(socket.gethostname())

class Caller:

    def __init__(self):
        self.status = "running"
        self.call_catcher_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.call_catcher_th = th.Thread(target=self.call_catch)
        self.call_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.used_ports = {5000: None}
    
    def _is_used(self, port):
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            test_sock.bind((IP, port))
        except socket.errno == errno.EADDRINUSE:
            test_sock.close()
            return True
        return False
    
    def start(self):
        self.call_catcher_th.start()
    
    def get_unused_port(self):
        last = 5000
        dirties = []
        for port in self.used_ports.keys():
            if port != 5000:
                if not self.used_ports[port].is_alive():
                    print(f"to remove: {port}")
                    dirties.append(port)
                if last != port - 1 and not self._is_used(last):
                    break
                last = port
        port = last + 1
        [self.used_ports.pop(key) for key in dirties]
        self.used_ports[port] = None
        return port
	
    def receive_run(self, src_port):
        receive_stream(IP, src_port)
        threads = self.used_ports.pop(src_port)

    def call_catch(self):
        self.call_catcher_sock.bind((IP, 5000))
        while self.status == "running":
            print("Wait for a call")
            data, addr = self.call_catcher_sock.recvfrom(1024)
            message = data.decode("utf-8").split(':')
            message_type = message[0]
            if message_type == "call":
                print(f"receive call: {message}")
                dst_port = int(message[1])
                src_port = self.get_unused_port()
                self.call_catcher_sock.sendto(f"{src_port}".encode('utf-8'), addr)
                communication = Communication(IP, src_port, addr[0], dst_port)
                self.used_ports[src_port] = communication
                communication.start()
    
    def call_send(self, name):
        self.call_send_sock.bind((IP, 4999))
        contact = get_contact(name)
        src_port = self.get_unused_port()
        self.call_send_sock.sendto(f"call:{src_port}".encode("utf-8"), (contact[1], 5000))
        data, addr = self.call_send_sock.recvfrom(1024)
        self.call_send_sock.close()
        dst_port = int(data.decode("utf-8"))
        communication = Communication(IP, src_port, contact[1], dst_port)
        self.used_ports[src_port] = communication
        communication.start()
        print("call sent")
    
import sys

caller = Caller()
if sys.argv[1] == "caller":
    caller.call_send(sys.argv[2])
else:
    caller.start()

