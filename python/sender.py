import socket
from main import stream

def send(buffer, sock, UDP_IP, UDP_PORT):
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

def send_stream(UDP_IP, UDP_PORT):
    print("sending video...")
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    stream(lambda buffer: send(buffer, sock, UDP_IP, UDP_PORT))


