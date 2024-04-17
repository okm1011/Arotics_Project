import socket
import struct
import numpy as np
import cv2
import pickle
import time
import threading
import queue

#HOST_RPI = '192.168.137.38'
#PORT = 8089
HOST_RPI = '172.30.1.12'
# host = AGV랑 소켓 연결하기위한 HOST_RPI
PORT = 8080

# 두개 소켓 cam for 수신 from AGV 카메라 mot for 방향 송신 to AGV control
client_cor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_cor.connect((HOST_RPI, PORT))
print("Socket connected")
time.sleep(10)

cmd = 1
cmd_byte = struct.pack('!B', cmd)
client_cor.sendall(cmd_byte)
