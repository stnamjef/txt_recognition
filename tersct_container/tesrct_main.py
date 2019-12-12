#!/usr/bin/python3
import tesrct_client as client
import socket
import cv2
import numpy
import os

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

TCP_PORT = 5000

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
    data = numpy.fromstring(stringData, dtype='uint8')

    print()
    print("    Successfully received.\n")

    decimg=cv2.imdecode(data,cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(filename, decimg)

    client.send_text(filename)

    os.remove(filename)

s.close()