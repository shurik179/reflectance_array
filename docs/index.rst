####################################
Reflectance Array with I2C interface
####################################
.. figure:: images/main.jpg
    :alt: reflectance array
    :width: 80%

This document describes the reflectanse array sensor created by `shurik179 <https://github.com/shurik179>`__. It is intended for use 
with small robots for tasks such as line following, sumo robots, and more.  All software and hardware 
files are available under an open source license from the project |github|; 
you can also buy a completed sensor from my Tindie store. 

Below are the key features of this sensor.

* **Dimensions:** 20x60 mm
* includes **6 individual reflectance sensors** (long range - 
  optimal distance to measured object is 4mm)
* has **i2c interface**, which supports normal (100k) and fast (400k) speeds
* contains an MCU (attiny 1616) which takes care of reading individual sensor input,  applying calibrations, and computing line position for line following tasks
* provides **qwiic/stemma qt connector** as well as standard 0.1" header connector (requires soldering)
* can be turned off to save batteries

.. toctree::
    :caption: Table of Contents
    :maxdepth: 1

    mechanical
    software_installation
    library
  
