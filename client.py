
#!/usr/bin/env python3

import socket
import selectors
import threading

sel = selectors.DefaultSelector()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 1241)
sock.connect(server_address)
sock.setblocking(False)

sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)
outgoing = []

def send_message():
    if len(outgoing) > 0:
        next_msg = outgoing.pop()
        print('sending {!r}'.format(next_msg))
        sock.sendall(next_msg)

def read_message(key):
    data = key.fileobj.recv(1024)
    if data:
        print('  received {!r}'.format(data))

def listener_server():
    while True:
        for key, mask in sel.select(timeout=1):
            if mask & selectors.EVENT_READ:
                read_message(key)
            if mask & selectors.EVENT_WRITE:
                send_message()

def user_input_event(sock):
    while True:
        user_input = input('->')
        outgoing.append(str.encode(user_input))


user_input = threading.Thread(target=user_input_event, args=(sock,))
listener_ser = threading.Thread(target=listener_server, args=())

user_input.start()
listener_ser.start()