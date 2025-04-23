# Reflectance array
This repository contains code, hardware design files and more  for a 6-sensor reflectance line array with i2c interface. 
It is work in progress.

Structure of the repository:
- docs: source files for readthedocs documentation 
- hardware: board design files (KiCad8)
- firmware: board firmware (Arduino sketch,using [megatinycore Arduino core](https://github.com/SpenceKonde/megaTinyCore))
- python_lib: library for using the sensor (Micropython/CircuitPython)
- 3d printed: various 3d printed mounts (including a mount for XRP robot)

## Features:
- 6 reflectance sensors (ITR1502; [datasheet](https://www.everlight.com.cn/wp-content/plugins/ItemRelationship/product_files/pdf/ITR1502SR40A-TR8.pdf))
- built-in MCU (attiny1616) takes care of reading the sensors and computing the calibrated reading 
- i2c interface; supports normal (100k) and fast (400k) speeds
- can be connected using [qwiic/stemma qt](https://www.sparkfun.com/qwiic) connector or standard 0.1" headers (need to be soldered)
- can be calibrated, setting black and white values for each sensor individually. Calibration values are preserved even when the sensor is powered off 
- built-in computation of line position for line following applications; supports white on black and black on white lines 
- built-in I2C pullups (3.3k) on SDA, SCL lines. Can be disabled by cutting open the solder bridge labeled "I2C pullups"
- configurable I2C address: default address is 0x11, but you can also configure the device to use I2C address 0x12, by closing the solder bridge jumper "I2C addr", thus allowing two sensors on the same I2C bus 
- provided library for use with micropython/circuitpython (Arduino library coming soon)

All of the above is distributed under open source license (MIT). See LICENSE file in this repositroy for details. 

## Usage
To use the sensor
- mount it to your robot so that the distance from bottom of PCB to the ground is about 6 mm and connect by a qwiic cable to your microcontroller. 
- for CircuitPython/micropython: upload the file 'linearray.py' to '/lib' folder on your microcontroller. For CircuitPython, you also need 'adafruit_bus_device' library; most boards with CircuitPython already include that library - see info at the library [github repository](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice)
- see included examples (in python_lib folder) for examples of usage
