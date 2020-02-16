## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

from Stepper import Stepper
from Servos import Servos

import time

MIN_VERTICAL_ANGLE = 0
MAX_VERTICAL_ANGLE = 120

LEFT_MIN_VERTICAL_ANGLE = 180
LEFT_MAX_VERTICAL_ANGLE = 60

RIGHT_MIN_VERTICAL_ANGLE = 10
RIGHT_MAX_VERTICAL_ANGLE = 100

SERVO_CHANNEL_LEFT = 15
SERVO_CHANNEL_RIGHT = 14

MIN_HORIZONTAL_ANGLE = -90
MAX_HORIZONTAL_ANGLE = +90

STEPPER_STEPS_PER_ANGLE = 513 / 360.0

class CameraMount:
    def __init__(self):
        self.stepper = Stepper()
        self.stepper_position_steps = 0

        self.servos = Servos()        
        self.servo_channel_left = SERVO_CHANNEL_LEFT
        self.servo_channel_right = SERVO_CHANNEL_RIGHT
        self.servo_angles_left = [LEFT_MIN_VERTICAL_ANGLE, LEFT_MAX_VERTICAL_ANGLE]
        self.servo_angles_right = [RIGHT_MIN_VERTICAL_ANGLE, RIGHT_MAX_VERTICAL_ANGLE]

        # [hack:] fine adjust left servo
        self.servos.servo_kit.servo[SERVO_CHANNEL_LEFT]._duty_range=5820
                    
    def __del__(self):
        del self.stepper
        del self.servos

    def rotateHorizontal(self, angle):
        angle = min(MAX_HORIZONTAL_ANGLE, max(MIN_HORIZONTAL_ANGLE, angle))
        steps_target = angle * STEPPER_STEPS_PER_ANGLE
        steps_diff = steps_target - self.stepper_position_steps
        self.stepper.step(int(abs(steps_diff)), steps_diff < 0)
        self.stepper_position_steps = steps_target

    def rotateVerticalLeft(self, angle):
        self.rotateVertical(self.servo_channel_left, angle, self.servo_angles_left)

    def rotateVerticalRight(self, angle):
        self.rotateVertical(self.servo_channel_right, angle, self.servo_angles_right)

    def rotateVertical(self, channel, angle, servo_angles):
        angle = min(MAX_VERTICAL_ANGLE, max(MIN_VERTICAL_ANGLE, angle))
        ratio = (angle - MIN_VERTICAL_ANGLE) / (MAX_VERTICAL_ANGLE - MIN_VERTICAL_ANGLE)
        servo_angle = servo_angles[0] + ratio * (servo_angles[1] - servo_angles[0])
        self.servos.rotate(channel, servo_angle)


if __name__ == '__main__':    
    camera_mount = CameraMount()
    time.sleep(1)

    for it in range(10):
        camera_mount.rotateVerticalLeft(30)
        camera_mount.rotateVerticalRight(50)
        
        time.sleep(2)
        
        camera_mount.rotateHorizontal(-45)
        time.sleep(0.5)
        camera_mount.rotateHorizontal(45)
        time.sleep(0.5)
        camera_mount.rotateHorizontal(0)
        time.sleep(1)
    
        camera_mount.rotateVerticalLeft(90)
        camera_mount.rotateVerticalLeft(30)
        camera_mount.rotateVerticalLeft(45)

        camera_mount.rotateVerticalRight(110)
        camera_mount.rotateVerticalRight(50)
        camera_mount.rotateVerticalRight(65)

        time.sleep(2)

        camera_mount.rotateHorizontal(-45)
        time.sleep(0.5)
        camera_mount.rotateHorizontal(45)
        time.sleep(0.5)
        camera_mount.rotateHorizontal(0)
        time.sleep(2)
    
    del camera_mount
