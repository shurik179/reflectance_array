# SPDX-FileCopyrightText: Copyright 2025 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT
# This file is part of reflectance sensor array sotware library: https://github.com/shurik179/reflectance_array
# 
# Line position test. Works best with line between 1/2" - 3/4" (12-20mm) wide
# Before running this test, make sure you had calibrated the sensor - see calibration.py example 

import time
from linearray import *

# YOU MUST UNCOMMENT ONE OF THE OPTIONS BELOW

# FOR MicroPython: uncomment two lines below
from machine import Pin, I2C
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
# end of micropython-specific block 

# FOR CircuitPython: Uncomment below. For i2c bus, you can use board.I2C() or board.STEMMA_I2C()
# import board 
# i2c = board.I2C()
# end of circuitpython-specific block 

# Common to both MP and CP:
# first argument is i2c bus
# second argument (optional) is I2C address; choices are 0x11 (default) or 0x12
# sensor = LineArray(i2c, 0x12)

sensor=LineArray(i2c)


print("Firmware version: {}".format(sensor.fw_version()))
time.sleep(1)
sensor.start()
# set mode. Options are 
# white line on black background: LINEMODE_WHITEONBLACK
# black line on white background: LINEMODE_BLACKONWHITE
sensor.set_linemode(LINEMODE_WHITEONBLACK)
time.sleep(3)

#now repeatedly print claibrated readings and line position     
while True:
    for s in range(6):
        value = sensor.calibrated(s)
        # formatted to take 4 characters, for better alignment
        print(f'{value:4}', end=' ')
    print(f'{sensor.line_pos():4}') #line position ranges from 0-100. 
    time.sleep(0.3)   