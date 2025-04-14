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
#start calibration
print("Starting calibration")
sensor.start_cal()
time.sleep(5)
#during this time, sensor should be moved so that each sensor sees both white and black 
sensor.end_cal()
#calibration complete
print("Calibration complete. Calibration values are shown below")
#print out calibration values. This is optional
print("Black White")
for s in range(6):
    black = sensor.get_cal_black(s)
    white = sensor.get_cal_white(s)
    print(f'{black:5} {white:5}')
time.sleep(3)
#now repeatedly print calibrated readings     
while True:
    for s in range(6):
        value = sensor.calibrated(s)
        # formatted to take 4 characters, for better alignment
        print(f'{value:4}', end=' ')
    print('') #just to end the line
    time.sleep(0.3)   