import RPi.GPIO as GPIO
from gpiozero import Servo
import time


"""
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN1,GPIO.OUT)
freq = 50
servo_pwm = GPIO.PWM(SERVO_PIN1, freq)
servo_pwm.start(50)
"""

STOP        = 0
RIGHT       = 1
LEFT        = 2
STRAIGHT    = 3

def PWMPercentage

class Car:

    def __init__(self, left_pin, right_pin, stopDistance = 20, freq = 50):

        """
        Car module for Raspberry pi

        attribute:
            
            freq: 
                Frequency of the car.

            status:
                Status of the car.
                signal:
                    0: stop
                    1: right
                    2: left
        """


        self.left_pin       = left_pin
        self.right_pin      = right_pin
        self.freq           = freq
        self.status         = STOP
        self.stopDistance   = stopDistance

        # Set PWM object
        self.left_pwm  = GPIO.PWM(self.left_pin , self.freq)
        self.right_pwm = GPIO.PWM(self.right_pin, self.freq)

        # Initialize duty cycle
        self.left_pwm.start(0)
        self.right_pwm.start(0)

        # Right direction duty cycle
        self.right_duty_max = 3
        self.right_duty_mid = 2
        self.right_duty_min = 1

        # Right direction duty cycle
        self.left_duty_max = 4
        self.left_duty_mid = 5
        self.left_duty_min = 6

    def GoStraight(self):

        print("Car starts to go straight.")
        self.left_pwm.ChangeDutyCycle(self.left_duty_mid)
        self.right_pwm.ChangeDutyCycle(self.right_duty_mid)
        
        self.status = STRAIGHT

    def TurnRight(self):
        """
        Make the car turn right.

        V-left > V-right

        pattern: left_max | right_mid

        """
        
        print("Car starts to turn right.")
        self.left_pwm.ChangeDutyCycle(self.left_duty_max)
        self.right_pwm.ChangeDutyCycle(self.right_duty_mid)
        
        self.status = RIGHT

    def TurnLeft(self):
        """
        Make the car turn left.

        V-left < V-right

        pattern: left_mid | right_max

        """

        print("Car starts to turn left.")
        self.left_pwm.ChangeDutyCycle(self.left_duty_mid)
        self.right_pwm.ChangeDutyCycle(self.right_duty_max)

        self.status = LEFT

    def Stop(self):
        """
        Stop the car instantly

        V-left = V-right = 0

        pattern: left_min | right_min

        """

        print("Stop the car.")
        self.left_pwm.ChangeDutyCycle(self.left_duty_min)
        self.right_pwm.ChangeDutyCycle(self.right_duty_min)

        self.status = STOP

    def GetStatus(self):

        return self.status


if __name__ == '__main__':
    SERVO_PIN1 = 18
    PIN2 = 12

    # GPIO.cleanup()

    GPIO.setwarnings(False)			#disable warnings
    GPIO.setmode(GPIO.BCM)		#set pin numbering system
    GPIO.setup(SERVO_PIN1,GPIO.OUT)
    freq = 50
    servo_pwm = GPIO.PWM(SERVO_PIN1, freq)		#create PWM instance with frequency
    servo_pwm.start(50)

    GPIO.setmode(GPIO.BCM)		#set pin numbering system
    GPIO.setup(PIN2,GPIO.OUT)
    freq = 50
    servo_pwm2 = GPIO.PWM(PIN2, freq)		#create PWM instance with frequency
    servo_pwm2.start(50)

    # servo_pwm.ChangeDutyCycle(0)
    # servo_pwm2.ChangeDutyCycle(0)

    #speed fast=2,12  slow=8
    # pwm: 2 -> 12.5
    # std = 12

    """
    moving forward
    2	12.5
    6	8.75

    turn right
    6	10.75

    turn left
    2	8.75

    """

    mutual_speed = 12
    another = ((2+12.5) - mutual_speed )
    dutyR = 2       # mutual_speed  # mutual_speed
    dutyL = 8.75    # another # std - mutual_speed
    # Loop for duty values from 2 to 12 (0 to 180 degrees)
    servo_pwm.ChangeDutyCycle(dutyR)
    servo_pwm2.ChangeDutyCycle(dutyL)
    run_time = 1.8
    time.sleep(run_time)
    dutyR = 6       # mutual_speed  # mutual_speed
    dutyL = 10.75    # another # std - mutual_speed
    # Loop for duty values from 2 to 12 (0 to 180 degrees)
    servo_pwm.ChangeDutyCycle(dutyR)
    servo_pwm2.ChangeDutyCycle(dutyL)
    time.sleep(run_time)
    servo_pwm.ChangeDutyCycle(0)
    servo_pwm2.ChangeDutyCycle(0)
        
    GPIO.cleanup()
