#!/usr/bin/env python

from Laser import Laser
import json
import datetime
import RPi.GPIO as GPIO
import time

GPIO_BUTTON = 26

laser = Laser()
start_time = datetime.datetime.now()
run_time = 0
engage = False

default_configuration = '{"run_time": 5, "min_movement": 10, "x_min": 0, "x_max": 90, "y_min": 0, "y_max": 30}'

def initiateLaserSequence():
    global engage
    # setup the push button GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    run = True
    
    # wire up a button press event handler to avoid missing a button click while the loop below
    # is busy processing something else.
    GPIO.add_event_detect(GPIO_BUTTON, GPIO.FALLING, callback=__button_handler, bouncetime=200)
    
    print ("running, press CTRL+C to exit...")
    try:
        while run:
            try:
                if(engage):
                    if(__run_time_elapsed()):
                        # we ran out of time for this run, shutdown the laser
                        engage = False
                        laser.stop()
                    else:
                        laser.fire()
                else:
                    # sleep here to lessen the CPU impact of our infinite loop
                    # while we're not busy shooting the laser. Without this, the CPU would
                    # be eaten up and potentially lock the Pi.
                    time.sleep(1)
                        
            except Exception as e:
                # swallowing exceptions isn't cool, but here we provide an opportunity to
                # print the exception to an output log, should crontab be configured this way
                # for debugging.
                print ('Unhandled exception: {0}'.format(str(e)))
            except KeyboardInterrupt:
                run = False
                print ('KeyboardInterrupt: user quit the script.')
                break
    finally:
        print ('Exiting program')
        laser.stop()
        GPIO.cleanup()

def __button_handler(channel):
    global engage
    
    print ('Button pressed! '.format(str(channel)))
    
    if(engage):
        print ('Already firing the laser, button press ignored')
    else:
        print ('Initiating Firing Sequence!')
        # only start a new firing sequence if we're not already in the middle of one.
        engage = True
        __calibrate_laser(None)

def __run_time_elapsed():
    # figure out if the laser has ran its course, and should be stopped.
    now = datetime.datetime.now()
    end_time = (start_time + datetime.timedelta(seconds=run_time)).time()
    
    if(now.time() > end_time):
        return True
    
    return False

def __calibrate_laser(configuration):
    global start_time
    global run_time
    
    if(configuration is None):
        # no user defined config, so we'll go with the defaults
        configuration = json.loads(default_configuration)
    
    print ("starting laser with config: {0}".format(configuration))
    
    start_time = datetime.datetime.now()
    
    run_time = configuration.get('run_time')
    min_movement = configuration.get('min_movement')
    x_max = configuration.get('x_max')
    x_min = configuration.get('x_min')
    y_max = configuration.get('y_max')
    y_min = configuration.get('y_min')
 
    laser.calibrate_laser(min_movement, x_min, x_max, y_min, y_max)

if __name__ == '__main__':
    initiateLaserSequence()