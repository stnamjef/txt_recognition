#!/usr/bin/python3

import socket
import cv2
import numpy
import pytesseract

def send_text(filename):
    TCP_IP = 'flask_server'
    TCP_PORT = 6000

    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT))

    stringData = pytesseract.image_to_string(filename, lang = 'eng')

    filename = filename.encode()
    sock.send(str(len(filename)).ljust(16).encode())
    sock.send(filename)
    stringData = stringData.encode()
    sock.send(str(len(stringData)).ljust(16).encode())
    sock.send(stringData)
    sock.close()