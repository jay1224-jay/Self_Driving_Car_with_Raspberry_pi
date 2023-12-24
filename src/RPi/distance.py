# Get distance from anything ahead

import RPi.GPIO as GPIO  # include
import time

GPIO.setmode(GPIO.BCM)
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

class disSensor:

    def __init__(self, pinTrigger, pinEcho, temperature = 25):

        self.pinTrigger = pinTrigger  
        self.pinEcho = pinEcho  

        # Celsius
        self.temperature = temperature

    def getDistance(self):


        GPIO.output(self.pinTrigger, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.pinTrigger, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(self.pinEcho) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(self.pinEcho) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # v = 331+0.6t
        # and divide by 2, because there and 
        soundSpeed = (331 + self.temperature)*100
        distance = (TimeElapsed * soundSpeed) / 2
        
        print("current distance: %.4fcm" % distance)
     
        return distance
