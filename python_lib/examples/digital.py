# SPDX-FileCopyrightText: Copyright 2025 Alexander Kirillov <shurik179@gmail.com>
# SPDX-License-Identifier: MIT
# This file is part of reflectance sensor array sotware library: https://github.com/shurik179/reflectance_array
# 
# Basic sensor digital test: checking if a given sensor is on black/on white
# Make sure you have run calibration before using this test 
# 

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
time.sleep(2)
sensor.start()
#print out current calibration values (optional)
print("current calibration")
print("Black White")
for s in range(6):
    black = sensor.get_cal_black(s)
    white = sensor.get_cal_white(s)
    print(f'{black:5} {white:5}')
time.sleep(3)
while True:
    for s in range(6):
        if (sensor.on_white(s)):
           print("1 ", end=' ')
        else:
            print("0 ", end=' ')
    if (sensor.all_white()):
        message = " all on white"
    elif (sensor.all_black()):
        message = " all on black "
    else:
        message = ' '
    print(message) #just to end the line
    time.sleep(0.3)