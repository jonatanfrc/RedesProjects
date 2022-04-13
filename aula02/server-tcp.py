#!/usr/bin/env python3

import socket

HOST = 'localhost' 
PORT = 50000       

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print('macarrão')
conn, ender = s.accept()

print('conectando em ', ender)
while True:
    data = conn.recv(1024)
    if not data:
        print('fechando a conexao')
        conn.close()
        break
    conn.sendall(data)