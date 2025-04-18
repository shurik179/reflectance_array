import time
import board 
from linearray import *
# first argument is i2c bus; typical choices are board.STEMMA_I2C() or board.I2C()
# second argument (optional) is I2C address; choices are 0x11 (default) or 0x12
# sensor = LineArray(board.I2C(), 0x12)
sensor=LineArray(board.STEMMA_I2C())
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