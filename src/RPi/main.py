import cv2,socket,pickle,os
import numpy as np

from car import Car
from distance import disSensor


# Initialization
myCar = Car(left_pin=10, right_pin=11, stopDistance=20)

host = "192.168.1.61"
port = 5000
client_socket = socket.socket()
client_socket.connect((host, port)) 
cap = cv2.VideoCapture(0) 

myDisSensor = disSensor(pinTrigger=18, pinEcho=24, temperature=20)

_direction = -1

def getDirection():
	global _direction
	return _direction

def clientObjTrackLoop():
	global _direction

	preMessage = ""
	while True:

	    ret,photo = cap.read()


	    # cv2.imshow('streaming',photo)
	    ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
	    x_as_bytes = pickle.dumps(buffer)
	    client_socket.send(x_as_bytes)
	    client_socket.send(b"stop")
	    
	    messageFromServer = client_socket.recv(1024).decode()

	        
	    """
	        Direction message:

	            0 stands for left
	            1 stands for right
	    """

	    if messageFromServer == "0" and messageFromServer != preMessage:
	        preMessage = "0"
	        print("Turn left")
	        _direction = 0

	    elif messageFromServer == "1" and messageFromServer != preMessage:
	        preMessage = "1"
	        print("Turn right")
	        _direction = 1

	    elif messageFromServer == "start" and messageFromServer != preMessage:
	        preMessage = "start"
	        print("Start objtracking")
	    
	    if cv2.waitKey(10)==ord('q'):
	        break

	cv2.destroyAllWindows()
	cap.release()

def mainLoop():

	direction = getDirection()

	currentDistance = myDisSensor.getDistance()

	if currentDistance <= myCar.stopDistance:
		
		myCar.Stop() 

	else:

		if direction == 0:
			myCar.TurnLeft()
		elif direction == 1:
			myCar.TurnRight()
		else:
			myCar.GoStraight()




# Threading

# TO-DO: Implement multi-threading

