import socket
import struct
import cv2
import pickle
import serial
import threading
from myagv import MyAgv
import numpy as np

#dsad

###########################################################################
def initMotor() :	
	print("init")

def goForward() :
	#print("goForward")
	# print("F")
	MA.go_ahead(1)

def stopMotor() :
	#print("stopMotor")
	# print("S")
	MA.stop()

def goBackward() :
	pass
	#print("goBackward")
	# print("B")
	# MA.retreat(20, timeout=1)
		
def turnLeft() :
	#print("turnLeft")
	# print("L")
	MA.counterclockwise_rotation(10)
		
def turnRight() :
	#print("turnRight")
	# print("R")
	MA.clockwise_rotation(10)

def exitMotor() :
	print("exitMotor")
  
#####################################################################  

initMotor()


# bot = Rosmaster()   # add
MA = MyAgv('/dev/ttyAMA2', 115200)

speedFwd = 30 #speed for 0~90
speedCurve = 30 #speed for 0~90


# VIDSRC = 'v4l2src device=/dev/video0 ! video/x-raw,width=160,height=120,framerate=20/1 ! videoscale ! videoconvert ! jpegenc ! appsink'

# cap=cv2.VideoCapture(VIDSRC, cv2.CAP_GSTREAMER)
cap = cv2.VideoCapture(0)

HOST = ''
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

server.bind((HOST, PORT))
print('Socket bind complete')

server.listen(10)
print('Socket now listening')

server_cam, addr = server.accept()
server_mot, addr = server.accept()
print('New Client.')

flag_exit = False
def mot_main() :

	while True:
		
		rl_byte = server_mot.recv(1)
		print(rl_byte)
		rl = struct.unpack('!B', rl_byte)
		#print(rl[0])
	
		right, left = (rl[0] & 2)>>1, rl[0] & 1
		#print(right, left )
		
		if not right and not left:
			goForward()
		elif not right and left:
			turnRight()
		elif right and not left:
			turnLeft()
		else:
			stopMotor()

		if flag_exit: break

motThread = threading.Thread(target=mot_main)
motThread.start()

try:

	while True:	

		cmd_byte = server_cam.recv(1)
		cmd = struct.unpack('!B', cmd_byte)
		# print(cmd[0])
		if cmd[0]==12 :	
		
			# capture camera data
			ret,frame=cap.read()
			# print(frame.shape)

			# data = frame

			# Serialize frame
			data = pickle.dumps(frame)
			# print(len(data))

			# send sensor + camera data
			data_size = struct.pack("!L", len(data)) 
			server_cam.sendall(data_size + data)
			
except KeyboardInterrupt:
	pass
except ConnectionResetError:
	pass
except BrokenPipeError:
	pass
except:
	pass

flag_exit = True
motThread.join()
	
server_cam.close()
server_mot.close()
server.close()

exitMotor()
