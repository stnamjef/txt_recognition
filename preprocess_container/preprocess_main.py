#!/usr/bin/python3
import page_dewarp_main as preprocess
import cv2
import numpy as np
import socket
import os
import sys
import datetime

def change_filename(filename):
    filename = filename.split(".")[0]
    filename += "_thresh.jpg"
    return filename

def send_img_processed(img, filename, container_name, tcp_port):
    TCP_IP = container_name
    TCP_PORT = tcp_port

    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', img, encode_param)
    stringData = imgencode.tostring()

    filename = filename.encode()
    sock.send(str(len(filename)).ljust(16).encode())
    sock.send(filename)
    sock.send(str(len(stringData)).ljust(16).encode())
    sock.send(stringData)
    sock.close()

# recieve an original image from a host

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
    filename = change_filename(filename)
    length = recvall(conn,16) 
    stringData = recvall(conn, int(length))
    data = np.fromstring(stringData, dtype='uint8')

    print()
    print("    Successfully received.\n")

    decimg=cv2.imdecode(data,cv2.IMREAD_COLOR)
    cv2.imwrite(filename, decimg)

    # image processing

    img_processed = preprocess.dewarp(filename)

    # send a pre-processed image to tesseract container & flask container

    
    send_img_processed(img_processed, filename, "flask_server", 4000)
    send_img_processed(img_processed, filename, "tesrct", 5000)

    # delete processed img

    os.remove("./" + filename)

s.close()