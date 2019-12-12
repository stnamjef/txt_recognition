#!/usr/bin/python3
import socket
import cv2

def send_img(filename):
    TCP_IP = 'preprocess'
    TCP_PORT = 4000

    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))

    filepath = './static/img/' + filename
    img = cv2.imread(filepath)

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', img, encode_param)
    stringData = imgencode.tostring()
    
    filename = filename.encode()
    sock.send(str(len(filename)).ljust(16).encode())
    sock.send(filename)
    sock.send(str(len(stringData)).ljust(16).encode())
    sock.send(stringData)
    sock.close()