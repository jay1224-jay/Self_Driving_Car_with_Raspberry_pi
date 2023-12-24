
import cv2, socket, numpy, pickle
import time
import sys

from server import Server


 
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

def middle_of_2_point(p1, p2):
    return ( int((p1[0]+p2[0])/2) , 
             int((p1[1]+p2[1])/2) )

colorYellow = (0, 255, 255)
colorBlack = (0, 0, 0)
colorGreen = (0, 255, 0)

client = "0.0.0.0"

if __name__ == '__main__' :
 
    myServer = Server(clientIP = client)

    frame = myServer.recvImageFromClient()

    frameHeight   = frame.shape[0]
    frameWidth    = frame.shape[1]
    frameChannels = frame.shape[2]
    print(f"Process resolution: {frameWidth}x{frameHeight}")

 
    myServer.sendMessageToClient("start")

    count = 0
 
    while True:

        frame = myServer.recvImageFromClient()

        myServer.sendMessageToClient("continue")

        timer = cv2.getTickCount()
 
 

        print("Streaming", count) 
        count += 1
        if ( count > 10 ):
            count = 0
     
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # Display FPS on frame
        if ( fps < 100 ):
            cv2.putText(frame, "FPS : " + str(int(fps)), (100,60), cv2.FONT_HERSHEY_SIMPLEX, 1, colorBlack, 2);
        else:
            cv2.putText(frame, "FPS : >100", (100,60), cv2.FONT_HERSHEY_SIMPLEX, 1, colorBlack, 2);

        cv2.putText(frame, "Live streaming only!!", (300,60), cv2.FONT_HERSHEY_SIMPLEX, 1, colorBlack, 2);
 
        # Display result
        cv2.imshow("Streaming", frame)

        if cv2.waitKey(1) == ord('q'):
            break


cv2.destroyAllWindows()
