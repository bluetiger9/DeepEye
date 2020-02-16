## Copyright (c) 2020 Attila Tőkés (tokes_atti@yahoo.com). All rights reserved.
## Licence: MIT

# ref: https://stackoverflow.com/questions/56410926/how-to-run-a-5v-stepper-motor-on-jetson-nano/59992156#59992156

import Jetson.GPIO as GPIO
import time

#DEFAULT_CONTROL_PINS = [18,17,27,22]
DEFAULT_CONTROL_PINS = ['DAP4_SCLK', 'UART2_RTS', 'SPI2_SCK', 'LCD_TE']
DEFAULT_STEP_TIME = 0.0005

IDLE_PATTERN = [0, 0, 0, 0]
HOLD_PATTERN = [1, 0, 0, 1]
HALFSTEP_SEQ = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
]

class Stepper:
    def __init__(self, control_pins = DEFAULT_CONTROL_PINS, step_time = DEFAULT_STEP_TIME):
        self.control_pins = control_pins
        self.step_time = step_time

        #GPIO.setmode(GPIO.BCM)
        GPIO.setmode(GPIO.TEGRA_SOC)
        for pin in self.control_pins:
            GPIO.setup(pin, GPIO.OUT)
        self._output(IDLE_PATTERN)

    def __del__(self):
        self._output(IDLE_PATTERN)
        GPIO.cleanup(self.control_pins)

    def halfStep(self, reverse = False):
        sequence = reversed(HALFSTEP_SEQ) if reverse else HALFSTEP_SEQ
        for pattern in sequence:
            self._output(pattern)
            time.sleep(self.step_time)

    def step(self, steps, reverse = False):
        for i in range(steps):
            self.halfStep(reverse)
            self._output(HOLD_PATTERN)
        self._output(IDLE_PATTERN)

    def _output(self, pattern):
        GPIO.output(self.control_pins, pattern)

