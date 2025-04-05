# Reflectance array
This repository contains code and hardware design files for a 6-sensor reflectance line array with i2c interface. 
It is work in progress.

Structure of the repository:
- hardware: board design files (KiCad8)
- firmware: board firmware (Arduino sketch,using [megatinycore Arduino core](https://github.com/SpenceKonde/megaTinyCore))
- circuitpython_lib: library for using the sensor (CircuitPython)

## Features:
- 6 reflectance sensors (ITR1502; [datasheet](https://www.everlight.com.cn/wp-content/plugins/ItemRelationship/product_files/pdf/ITR1502SR40A-TR8.pdf))
- i2c interface; supports normal (100k) and fast (400k) speeds
- can be calibrated, setting black and white values for each sensor individually
- built-in MCU (attiny1616) takes care of reading the sensors and computing the calibrated reading 
- built-in computation of line position for line following applications; supports white on black and black on white lines 

All of the above is distributed under open source license (MIT). See LICENSE file in this repositroy for details. 
