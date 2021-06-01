#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import threading, time


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello,%s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)


s = socket.socket()
s.bind(('127.0.0.1', 1234))
s.listen(5)
print('Waiting for conection...')

while True:
    # accept a new connection
    sock, addr = s.accept()
    # create a new thread
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.setDaemon(True)
    t.start()