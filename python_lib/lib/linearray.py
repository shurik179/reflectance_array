# SPDX-FileCopyrightText: Copyright 2025 Alexander Kirillov <shurik179@gmail.com>
#
# SPDX-License-Identifier: MIT

"""
`linearray`
====================================================

This is a CircuitPython/micropython library for Line Array sensor by Alexander Kirillov.
If used with CircuitPython, requires adafruit_bus_device library

* Author(s): Alexander Kirillov
* Version: 1.0
"""

import time
import sys

# MP will be True if interpreter is micropython; otherwise, we assume Circuti Python
MP =(sys.implementation.name == 'micropython')

#print(MP)
    

if MP:
    # import micropython libraries 
    from machine import Pin, I2C
else:
    # import circuit python libraries
    import board
    from adafruit_bus_device.i2c_device import I2CDevice
    from digitalio import DigitalInOut, Direction, Pull

LINEARRAY_I2C_ADDR =const(0x11)
MODE_ON = const(1)
MODE_OFF = const(0)
MODE_CAL = const(2)
MODE_CAL_END = const(3)
LINEMODE_BLACKONWHITE = const(0)
LINEMODE_WHITEONBLACK = const(1)
NUM_SENSORS = const(6)
REG_WHOAMI = const(0)
REG_MODE = const (1)
REG_LINE_MODE = const (2)
REG_FW_MINOR = const(3)
REG_FW_MAJOR = const (4)
REG_SENSOR_RAW = const(6)
REG_SENSOR_CAL = const(18)
REG_SENSOR_DIGITAL = const(30)
REG_LINE_POS = const (31)
REG_CALIBRATIONS = const(32)

class LineArray:
    def __init__(self, i2c, address=LINEARRAY_I2C_ADDR):
        if MP:
            #micropython
            self._i2c = i2c
            self._address = address
        else:
            #circuitpython
            self._device = I2CDevice(i2c, address, probe = False)
        try:
            chipid = self._read_8(REG_WHOAMI)
        except:
            chipid = 0
            #i2c.unlock()
            print("Failed to find the sensor")
        if chipid != 0:
            print("Found sensor with ID {}".format(hex(chipid)))

######## Firmware version
    def fw_version(self):
        """Returns firmware version as a string"""
        minor = self._read_8(REG_FW_MINOR)
        major = self._read_8(REG_FW_MAJOR)
        return("{}.{}".format(major,minor))
    
#######  Setting mode 
    def start(self):
        self._write_8(REG_MODE, MODE_ON)

    def stop(self):
        self._write_8(REG_MODE, MODE_OFF)

    def start_cal(self):
        self._write_8(REG_MODE, MODE_CAL)

    def end_cal(self):
        self._write_8(REG_MODE, MODE_CAL_END)


####### Reading sensor 
    def raw(self, i):
        if (i>=NUM_SENSORS):
            return(0) #out of range 
        return (self._read_16(REG_SENSOR_RAW+2*i))

    def calibrated(self, i):
        if (i>=NUM_SENSORS):
            return(0) #out of range 
        return (self._read_16(REG_SENSOR_CAL+2*i))

    def all_black(self):
        #0x3F = 0b00111111 
        data = self._read_8(REG_SENSOR_DIGITAL) &0x3F
        return ( data == 0)  
    
    def all_white(self):
        #0x3F = 0b00111111 
        data = self._read_8(REG_SENSOR_DIGITAL) &0x3F
        return ( data == 0x3F)  
    
    def on_white(self, i):        
        return bool(self._read_8(REG_SENSOR_DIGITAL) & (1<<i))

    def on_black(self, i):        
        return (not bool(self._read_8(REG_SENSOR_DIGITAL) & (1<<i)))
####### Reading line position
    
    def set_linemode(self, mode):
        self._write_8(REG_LINE_MODE, mode)

    def line_pos(self):
        return(self._read_8(REG_LINE_POS))
    
    
####### Reading calibration values 
    def get_cal_black(self, s):
        return (self._read_16(REG_CALIBRATIONS+4*s))
    def get_cal_white(self, s):
        return (self._read_16(REG_CALIBRATIONS+4*s+2))
    
    

##########  I2C UTILITY  ########################################
    def _write_8(self, register, data):
        # Write 1 byte of data to the specified  register address.
        # data must be a byte
        if MP:
            self._i2c.writeto_mem(self._address, register & 0xFF, bytes([data]) )
        else: 
            with self._device:
                self._device.write(bytes([register & 0xFF, data]))

    def _read_8(self, register):
        # Read and return a byte from  the specified register address.
        if MP:
            self._i2c.writeto(self._address, bytes([register & 0xFF]))
            result = self._i2c.readfrom(self._address, 1)
            return result[0]
        else:        
            with self._device:
                result = bytearray(1)
                self._device.write(bytes([register & 0xFF]))
                self._device.readinto(result)
                #self._device.write_then_readinto(bytes([address & 0xFF]),result)
                return result[0]
        
    def _read_16(self, register):
        # Read and return an unsigned 16bit int from  the specified register address (low byte at address, high byte at address+1)
        if MP:
            self._i2c.writeto(self._address, bytes([register & 0xFF]))
            result = self._i2c.readfrom(self._address, 2)
            return (result[0]|(result[1]<<8))

        else:       
            with self._device:
                result = bytearray(2)
                self._device.write(bytes([register & 0xFF]))
                self._device.readinto(result)
                return (result[0]|(result[1]<<8))
                    
