import cv2,socket,pickle,os
import numpy as np
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1000000)
server_ip = "localhost"
server_port = 6666

cap = cv2.VideoCapture(-1)  # use 0 if not using Raspberry Pi camera slot



while True:

    ret,photo = cap.read()
    # print(photo[0], photo[1])

    # cv2.imshow('streaming',photo)
    ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
    x_as_bytes = pickle.dumps(buffer)
    print("send message to server")
    s.sendto((x_as_bytes),(server_ip,server_port))
    

    messageFromServer = s.recv(1024).decode()

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
    # print(messageFromServer)

    if cv2.waitKey(10)==ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
