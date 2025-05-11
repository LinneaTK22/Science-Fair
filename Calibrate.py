import RPi.GPIO as GPIO
import time

GPIO_X_SERVO = 4
GPIO_Y_SERVO = 17

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(GPIO_X_SERVO, GPIO.OUT)
    GPIO.setup(GPIO_Y_SERVO, GPIO.OUT)

    print ("calibrating...")
    try:
        x_servo = GPIO.PWM(GPIO_X_SERVO, 50)
        y_servo = GPIO.PWM(GPIO_Y_SERVO, 50)
        
        x_servo.start(7.5)  # X Servo: 7.5 is 90 degrees
        y_servo.start(2.5)  # Y Servo: 2.5 is 0 degrees

        time.sleep(1) # give the servos a chance to move
        
    finally:
        print("Clean up")
        GPIO.cleanup()