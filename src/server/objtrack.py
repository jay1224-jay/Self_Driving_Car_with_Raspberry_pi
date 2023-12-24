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
    # myServer.sendMessageToClient("Hello from server")

    frame = myServer.recvImageFromClient()

    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]
    # tracker_type = tracker_types[7]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
        if tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()
 
 
    time.sleep(2)
    bbox = cv2.selectROI(frame, False)

    # myServer.sendMessageToClient("3")
 
    ok = tracker.init(frame, bbox)


 
    while True:

        myServer.sendMessageToClient("goon")
        frame = myServer.recvImageFromClient()

        timer = cv2.getTickCount()
 
        ok, bbox = tracker.update(frame)
 
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        ratio = 3
        if ok:

            """

            # draw direction

            print(bbox)
            # Tracking success

            if ( pre_point == (-1, -1) ):
                pre_point = middle_of_2_point(p1, p2)
            else:
                # middle_point = (int(bbox[0] + bbox[2]/2), int(bbox[1] + bbox[3]/2))
                middle_point = middle_of_2_point(p1, p2)

            dx = middle_point[0] - pre_point[0]
            dy = middle_point[1] - pre_point[1]

            if ( (dx**2 + dy**2)**0.5 < 2 ):
                dx *= 10 # ratio
                dy *= 10 # ratio

            
            # end_point = (1000, 100)
            end_point = (   int((middle_point[0]+dx*ratio)), 
                            int((middle_point[1]+dy*ratio)) )
 
            cv2.arrowedLine(frame, middle_point, end_point, (0, 255, 0), 3)

            pre_point = middle_point

            print("middle point:", middle_point, ", dx:", dx, ", dy:", dy)
            """


            # draw to center
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

            # the line pointing to the center

            frameHeight   = frame.shape[0]
            frameWidth    = frame.shape[1]
            frameChannels = frame.shape[2]

            centerPoint = [int(frameWidth/2), int(frameHeight/2)]

            currentPoint = middle_of_2_point(p1, p2)

            # opencv color : (b, g, r)
            cv2.arrowedLine(frame, currentPoint, centerPoint, colorYellow, 3)

            # show car direction message

            directionMessage = ""
            if centerPoint[0] - currentPoint[0] > 0:
                directionMessage = "Turn Left"
                myServer.sendMessageToClient("0")
            else:
                directionMessage = "Turn Right"
                myServer.sendMessageToClient("1")

            cv2.putText(frame, directionMessage, (int(frameWidth/2),30), cv2.FONT_HERSHEY_SIMPLEX, 1, colorYellow,2);

        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,30), cv2.FONT_HERSHEY_SIMPLEX, 1, colorGreen,2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,60), cv2.FONT_HERSHEY_SIMPLEX, 1, colorGreen, 2);
 
        # Display result
        cv2.imshow("Tracking", frame)

        if cv2.waitKey(1) == ord('q'):
            break


cv2.destroyAllWindows()
