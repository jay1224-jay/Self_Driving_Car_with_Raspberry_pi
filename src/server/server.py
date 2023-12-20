import cv2, socket, numpy, pickle
import time


class Server:

    def __init__(self, clientIP):
        print("start building socket...")
        self.s=socket.socket()
        self.host = socket.gethostname()
        print(self.host)
        self.ip=clientIP
        self.port=6666
        self.s.bind((self.host,self.port))
        self.s.listen(2)
        self.conn, address = self.s.accept()
        print("Connection from: " + str(address))
        print("connect successfully")

 
    def recvImageFromClient(self):

        x=self.conn.recvfrom(1000000)
        self.data=x[0]
        self.data=pickle.loads(self.data)
        self.data = cv2.imdecode(self.data, cv2.IMREAD_COLOR)

        return self.data

    def sendMessageToClient(self, message):

        """
        
        Direction message:

            0 stands for left
            1 stands for right

        """

        self.conn.send(message.encode())

