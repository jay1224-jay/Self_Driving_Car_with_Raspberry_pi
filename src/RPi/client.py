import cv2,socket,pickle,os
import numpy as np
s=socket.socket()
server_ip = socket.gethostname()
server_port = 6666

s.connect((server_ip, server_port))

cap = cv2.VideoCapture(-1)  # use 0 if not using Raspberry Pi camera slot


preMessage = ""
while True:

    ret,photo = cap.read()
    # print(photo[0], photo[1])

    # cv2.imshow('streaming',photo)
    ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
    x_as_bytes = pickle.dumps(buffer)
    # print("send message to server")
    
    # s.sendto((x_as_bytes),(server_ip,server_port))
    s.send(x_as_bytes)

    # print("Client waiting for message from server")

    messageFromServer = s.recv(1024).decode()
    if messageFromServer == "0" and preMessage != "0":
        print("Turn left   <--")
        preMessage = "0"
    elif messageFromServer == "1" and preMessage != "1":
        print("Turn right  -->")
        preMessage = "1"
    elif messageFromServer == "3" and preMessage != "2":
        print("Start objtracking")
        preMessage = "2"

    
    if cv2.waitKey(10)==ord('q'):
        break

s.close()
cv2.destroyAllWindows()
cap.release()
