#!/usr/bin/python3

import socket
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def change_name(filename):
    filename = filename.split(".")[0]
    filename += ".txt"
    return filename


TCP_PORT = 6000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(True)

while True: 
    conn, addr = s.accept()

    length = recvall(conn, 16)
    filename = recvall(conn, int(length))
    filename = filename.decode()
    filename = change_name(filename)
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    stringData = stringData.decode()

    f = open("./static/text/" + filename, "w", encoding="utf-8")
    for word in stringData:
        f.write(word)
    f.close()

s.close()