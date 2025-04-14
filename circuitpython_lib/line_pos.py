import time
import board 
from linearray import *
# first argument is i2c bus; typical choices are board.STEMMA_I2C() or board.I2C()
# second argument (optional) is I2C address; choices are 0x11 (default) or 0x12
# sensor = LineArray(board.I2C(), 0x12)
sensor=LineArray(board.STEMMA_I2C())
print("Firmware version: {}".format(sensor.fw_version()))
time.sleep(1)
sensor.start()
print("Calibration values")
#print out calibration values. This is optional
print("Black White")
for s in range(6):
    black = sensor._read_16(32+4*s)
    white = sensor._read_16(32+4*s+2)
    print(f'{black:5} {white:5}')
sensor.set_linemode(LINEMODE_WHITEONBLACK)
time.sleep(3)

#now repeatedly print calibrated readings     
while True:
    for s in range(6):
        value = sensor.calibrated(s)
        # formatted to take 4 characters, for better alignment
        print(f'{value:4}', end=' ')
    print(f'{sensor.line_pos():4}') #just to end the line
    time.sleep(0.3)   