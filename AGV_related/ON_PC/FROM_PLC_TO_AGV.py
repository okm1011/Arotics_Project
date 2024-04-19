import socket
import struct
import numpy as np
import cv2
import pickle
import time
import threading
import queue
import serial

def init_server():
    #HOST_RPI = '192.168.137.38'
    #PORT = 8089
    HOST_RPI = '172.30.1.36'
    # host = AGV랑 소켓 연결하기위한 HOST_RPI
    PORT = 8080

    # 두개 소켓 cam for 수신 from AGV 카메라 mot for 방향 송신 to AGV control
    client_cor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_cor.connect((HOST_RPI, PORT))
    print("Socket connected")
    time.sleep(10)
    return client_cor
def init_serial():
    py_serial=serial.Serial(

        port='COM1',
        # com x번을 사용해서 serial 통신
        baudrate=115200,
    )
    return py_serial

client_cor = init_server();
py_serial = init_serial();
while True:
    if py_serial.readable():

        # 들어온 값이 있으면 값을 한 줄 읽음 (BYTE 단위로 받은 상태)
        # BYTE 단위로 받은 response 모습 : b'\xec\x97\x86\xec\x9d\x8c\r\n'
        response = py_serial.readline()
            
        # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
        value = response[:len(response)-1].decode()
        if(int(value) == 1):
            cmd = 1
            cmd_byte = struct.pack('!B', cmd)
            client_cor.sendall(cmd_byte)
