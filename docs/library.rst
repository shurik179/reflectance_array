.. _library:
**************************
Python Library Reference
**************************

In this chapter, we give full list of all commands provided by refelectance 
array micropython/Circuit Python library.

This document describes version 1.0 of the library. It assumes that you 
had already created object LineArray object; all methods below are methods 
of this object (e.g. ). Sensor index s ranges from 0--5


Basic commands
==============

.. function:: start()
.. function:: stop() 

    Starting and stopping the sensor. By default, the sensor is active. To save battery, 
    you can stop it by using `stop()`; this turns off the power to IR LEDs inside reflectance 
    sensors.  Note that you can still read the reflectance sensor values even when the LEDs are off; 
    this can be useful for detecting ambient light changes.

.. function:: fw_version()

    Returns firmware version as a string, e.g. `1.3`

.. function:: raw(s)

   Returns raw reading of  s-th reflection sensor (0-1023). The darker the surface, 
   the lower the value. Typical value on a white sheet of paper is around 950, 
   and on black plastic, around 120. 


Calibration
===========
You can calibrate the sensor, recording  values for black and white; these values 
will be used for computing calibrated readings and for deciding when the sensor 
is on black/white (see below). 

 The calibration values are saved in EEPROM, which means that they are preserved  
 even when you turn off the  power to the sensor; they  will be loaded on next power-up. 



.. function:: start_cal()
.. function:: end_cal()

   Starts and stops calibration. In between these commands, it is expected that 
   you move the robot so that each sensor sees both white and black. The lowest 
   recorded value will be saved as black calibration, and the highest, as white 
   calibration; these are saved individaully per sensor.

.. function:: get_cal_black(s)
.. function:: get_cal_white(s)

   Returns the value of black (respectively, white) calibration for sensor s. 
   This is rarely needed - mostly to verify that calibration was successful 
   in cases when your sensor behaves unexpectedly. 
   

Calibrated readings
===================
.. function:: calibrated(s)

   This function assumes that you had already calibrated your sensor. It returns 
   calibrated value. For example, if calibration values were 300 (black) and 800 (white)
   then raw reading of 300 or less  will give calibrated reading 0, raw reading of 800 
   or above will give calibrated reading of 1023, and all values in between will be 
   rescaled linearly - e.g., raw reading of 550 (which is exactly the midpoint between 300 and 800)
   will give calibrated reading of 512. 

Digital readings
================  
In many cases you only need to know if the sensor is on black/white and not interested in exact reading. 
In these cases, it is much faster to use the functions below. As before, you should calibrate 
your sensor before using these functiosn. 

.. function:: on_black(s)
.. function:: on_white(s)

   Returns True if sensor s is on black (respectively, white) and False otherwise. 
   The cutoff between white and black is defined to be the  midpoint between black 
   and white calibration values. 

.. function:: all_black()
.. function:: all_white()

   Returns True if all sensors are on black (respectively, white) and False otherwise. 





