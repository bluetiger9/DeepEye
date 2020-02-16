## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

from adafruit_servokit import ServoKit
import time

DEFAULT_ANGLE = 50
MAX_CHANNEL = 15

class Servos:
    def __init__(self):
        self.servo_kit = ServoKit(channels=16)
        for channel in range(0, MAX_CHANNEL + 1):
            self.servo_kit.servo[channel].angle = DEFAULT_ANGLE
            #self.rotate(servo, DEFAULT_ANGLE)
                    
    def __del__(self):
        for channel in range(0, MAX_CHANNEL + 1):
            self.servo_kit.servo[channel].angle = DEFAULT_ANGLE
            #self.rotate(servo, DEFAULT_ANGLE)

    def rotate(self, channel, angle):
        current = int(self.servo_kit.servo[channel].angle)
        #print("rotate: ", current, angle)
        if angle > current:
            #print("forward: ", current, int(angle))
            angle_range = range(current, int(angle))
        else:
            #print("reversed: " , int(angle), current)
            angle_range = reversed(range(int(angle), current))

        for step in angle_range:
            #print(step)
            self.servo_kit.servo[channel].angle = step
            time.sleep(0.005)
