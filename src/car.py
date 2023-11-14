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

class Car:

    def __init__(self, left_pin, right_pin, freq = 50):

        self.left_pin  = left_pin
        self.right_pin = right_pin
        self.freq      = freq

        # Set PWM object
        self.left_pwm  = GPIO.PWM(self.left_pin , self.freq)
        self.right_pwm = GPIO.PWM(self.right_pin, self.freq)

        # Initialize duty cycle
        self.left_pwm.start(0)
        self.right_pwm.start(0)







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
