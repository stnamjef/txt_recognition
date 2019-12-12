#!/usr/bin/python3

import socket
import cv2
import numpy as np

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_PORT = 4000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', TCP_PORT))
s.listen(True)

while True:
    conn, addr = s.accept()

    length = recvall(conn, 16)
    filename = recvall(conn, int(length))
    filename = filename.decode()
    length = recvall(conn,16) 
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')

    print()
    print("    Successfully received.\n")

    decimg=cv2.imdecode(data,cv2.IMREAD_GRAYSCALE)
    cv2.imwrite("./static/img_processed/" + filename, decimg) # has been changed

s.close()