import RPi.GPIO as GPIO
import time

GPIO_LASER = 27

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_LASER, GPIO.OUT)

    print('blinking laser...')
    try:  
        # Test turning the laser on and off
        time.sleep(1)
        GPIO.output(GPIO_LASER, 1)
        time.sleep(1)
        GPIO.output(GPIO_LASER, 0)
        time.sleep(1)
        GPIO.output(GPIO_LASER, 1)
        time.sleep(1)
        GPIO.output(GPIO_LASER, 0)

    finally:
        GPIO.output(GPIO_LASER, 0)
        GPIO.cleanup()