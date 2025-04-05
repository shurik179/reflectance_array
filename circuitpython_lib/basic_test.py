import time
from linearray import *
sensor=LineArray()
print("Firmware version: {}".format(sensor.fw_version()))
sensor.start()
while True:
    reading = sensor._read_8(30);
    print(sensor.all_white())
    