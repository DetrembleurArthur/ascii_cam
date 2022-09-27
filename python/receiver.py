import socket
from main import stream


def receive_stream(UDP_IP, UDP_PORT):
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.settimeout(5)
    sock.bind((UDP_IP, UDP_PORT))
    print('waiting for video...')
    try:
        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
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