**********************
Software installation
**********************

The sensor comes with a micropython/circuit python library, which can be found in the |github|. 
To use it, please download the latest release archive file from https://github.com/shurik179/reflectance_array/releases. 
Extract the archive file to a convenient location and find inside folder 'python_lib', which contains the library 
and example code. Upload the file 'lib/linearray.py' to '/lib' folder on your microcontroller (the same file can 
be used both for micropython and Circuit Python).

For Circuit Python, you also need 'adafruit_bus_device' library; most boards with CircuitPython 
already include that library - see info at the 
library `github repository  <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`__

The following python code gives the simplest example of using this library.

Micropython (make sure to use correct i2c pin numbers)

.. code-block:: python

    import time
    from linearray import *
    from machine import Pin, I2C
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
    sensor=LineArray(i2c)
    print("Firmware version: {}".format(sensor.fw_version()))
    time.sleep(2)
    sensor.start()
    while True:
        for s in range(6):
            value = sensor.raw(s)
            # formatted to take 4 characters, for better alignment
            print(f'{value:4}', end=' ')
        print('') #just to end the line
        time.sleep(0.3)

Circuit Python (you may need to replace 'board.I2C()' by 'board.STEMMA_I2C()', see https://learn.adafruit.com/circuitpython-essentials/circuitpython-i2c)

.. code-block:: python

    import time
    from linearray import *
    import board 
    i2c = board.I2C()
    sensor=LineArray(i2c)
    print("Firmware version: {}".format(sensor.fw_version()))
    time.sleep(2)
    sensor.start()
    while True:
        for s in range(6):
            value = sensor.raw(s)
            # formatted to take 4 characters, for better alignment
            print(f'{value:4}', end=' ')
        print('') #just to end the line
        time.sleep(0.3)


The folder 'Examples' contains several code examples:

* basic_test.py: the basic example - same code as given above
* calibration.py: example of sensor calibration 
* digital.py: when you only need to know if a given sensor is on white/black 
* line_pos.py: getting the position of the line under your robot, for line following 

For a full list of all available methods provided by this library, see :ref:`Python Library <library>`.