import cv2,socket,pickle,os
import numpy as np
host = "192.168.1.61" # socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server

cap = cv2.VideoCapture(-1)  # use 0 if not using Raspberry Pi camera slot

while True:

    ret,photo = cap.read()
    # print(photo[0], photo[1])

    cv2.imshow('streaming',photo)
    ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),20])
    x_as_bytes = pickle.dumps(buffer)
    print("send message to server")
    # s.sendto((x_as_bytes),(server_ip,server_port))
    print(x_as_bytes, len(x_as_bytes))
    client_socket.send(x_as_bytes)
    client_socket.send(b"stop")
    
    messageFromServer = client_socket.recv(1024).decode()

        
    """
        Direction message:

            0 stands for left
            1 stands for right
    """
    if messageFromServer == "0":
        print("Turn left")
    elif messageFromServer == "1":
        print("Turn right")
    elif messageFromServer == "3":
        print("Start objtracking")
    print(messageFromServer)

    if cv2.waitKey(10)==ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
