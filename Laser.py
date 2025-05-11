import time
import RPi.GPIO as GPIO # type: ignore
import random

DEFAULT_RUN_TIME = 90
DEFAULT_MIN_MOVEMENT = 10
DEFAULT_X_MIN_POSITION = 40
DEFAULT_X_MAX_POSITION = 120
DEFAULT_Y_MIN_POSITION = 20
DEFAULT_Y_MAX_POSITION = 60

# Define which GPIO pins to use for the servos and laser
GPIO_X_SERVO = 4
GPIO_Y_SERVO = 17
GPIO_LASER = 27

class Laser:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.x_servo = None
        self.y_servo = None

        GPIO.setup(GPIO_X_SERVO, GPIO.OUT)
        GPIO.setup(GPIO_Y_SERVO, GPIO.OUT)
        GPIO.setup(GPIO_LASER, GPIO.OUT)

    def calibrate_laser(self, min_movement, x_min, x_max, y_min, y_max):
        # set config variables, using the defaults if one wasn't provided
        self.min_movement = DEFAULT_MIN_MOVEMENT if min_movement is None else min_movement
        self.x_min = DEFAULT_X_MIN_POSITION if x_min is None else x_min
        self.x_max = DEFAULT_X_MAX_POSITION if x_max is None else x_max
        self.y_min = DEFAULT_Y_MIN_POSITION if y_min is None else y_min
        self.y_max = DEFAULT_Y_MAX_POSITION if y_max is None else y_max

        # start at the center of our square/ rectangle.
        self.x_position = x_min + (x_max - x_min) / 2
        self.y_position = y_min + (y_max - y_min) / 2

        # turn on the laser and configure the servos
        GPIO.output(GPIO_LASER, 1)
        self.x_servo = GPIO.PWM(GPIO_X_SERVO, 50)
        self.y_servo = GPIO.PWM(GPIO_Y_SERVO, 50)

        # start the servo which initializes it, and positions them center on the cartesian plane
        self.x_servo.start(self.__get_position(self.x_position))
        self.y_servo.start(self.__get_position(self.y_position))

         # give the servo a chance to position itself
        time.sleep(1)

    def fire(self):
        self.movement_time = self.__get_movement_time()
        print("Movement time {0}" .format(self.movement_time))
        print("Current position: X:{0}, Y:{1}" .format(self.x_position, self.y_position))

        # how many steps (how long) should we take to get from old to new position
        self.x_incrementer = self.__get_position_incrementer(self.x_position, self.x_min, self.x_max)
        self.y_incrementer = self.__get_position_incrementer(self.y_position, self.y_min, self.y_max)

        for index in range(self.movement_time):
            print("In For, X Position: {0}, Y Position: {1}" .format(self.x_position, self.y_position))
            self.x_position += self.x_incrementer 
            self.y_position += self.y_incrementer

            self.__set_servo_position(self.x_servo, self.x_position)
            self.__set_servo_position(self.y_servo, self.y_position)

            time.sleep (0.02)

        time.sleep(self.__get_movement_delay())

    def stop(self):
        print("\n Tidying up")
        if(self.x_servo is not None):
            self.x_servo.stop()

        if(self.y_servo is not None):
            self.y_servo.stop()

        GPIO.output(GPIO_LASER, 0)

    def __set_servo_position(self, servo, position):
        servo.ChangeDutyCycle(self.__get_position(position))

    def __get_position(self, angle):
        return(angle/18) + 2.5

    def __get_position_incrementer(self, position, min, max):
        newPosition = random.randint(min + self.min_movement, max - self.min_movement)
        print("New Position: {0}".format(newPosition))

        # how many steps (how long) should we take to get from old to new position
        if((newPosition > position) and (abs(newPosition - position)) < self.min_movement):
            newPosition += self.min_movement
        elif((newPosition < position) and (abs(newPosition - position)) < self.min_movement):
            newPosition -= self.min_movement

        # return the number of steps, or incrementer, we should take to get to the new position
        # this is a convenient way to slow the movement down, rather than seeing very rapid movements
        # from point A to point B
        return float((newPosition - position) / self.movement_time)
    
    def __get_movement_delay(self):
        return random.uniform(0, 1)
    
    def __get_movement_time(self):
        return random.randint(10, 40)
    
    