import cv2, socket, numpy, pickle
import time


class Server:

    def __init__(self, clientIP):
        print("start building socket...")
        self.s=socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
        self.ip=clientIP
        self.port=6666
        self.s.bind((self.ip,self.port))
        print("connect successfully")

 
    def recvImageFromClient(self):

        x=self.s.recvfrom(1000000)
        clientip = x[1][0]
        self.data=x[0]
        self.data=pickle.loads(self.data)
        self.data = cv2.imdecode(self.data, cv2.IMREAD_COLOR)

        return self.data


