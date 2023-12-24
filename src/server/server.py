import cv2, socket, numpy, pickle
import time


class Server:

    def __init__(self, clientIP):
        print("start building socket...")
        self.s=socket.socket()
        self.ip=clientIP
        self.port=5000
        self.s.bind((self.ip,self.port))
        self.s.listen(10)
        self.conn, address = self.s.accept()
        print("Connection from: " + str(address))
        print("connect successfully")

 
    def recvImageFromClient(self):

        image = b""
        while True:
            # print("wait for recv")
            x=self.conn.recv(1000000)
            # print("recved")
            # print("keep recv partial msg, x = ", x, len(x))
            image += x
            if x[-4:] == b'stop':
                image = image[:-4]
                break
        self.data = image
        # print(self.data)
        # print(len(image))
        self.data=pickle.loads(image)
        self.data = cv2.imdecode(self.data, cv2.IMREAD_COLOR)

        return self.data

    def sendMessageToClient(self, message):

        """
        
        Direction message:

            0 stands for left
            1 stands for right

        """

        self.conn.send(message.encode())

