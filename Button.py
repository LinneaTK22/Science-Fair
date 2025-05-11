import RPi.GPIO as GPIO
import time

GPIO_BUTTON = 26
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    print ('Press the button 3 times to exit...')

    press_count = 0
    while press_count < 3:
        # Test pressing of the button!
        button_pressed = GPIO.input(GPIO_BUTTON) == False
        if(button_pressed):
            print('Button Pressed!') 
            press_count += 1

            # pause to avoid the button press being picked up multiple times
            time.sleep(0.5)
    
    GPIO.cleanup()