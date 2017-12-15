"""
direct serial communication with TDS3000C & TDS3GM
python 2.7 (http://www.python.org/)
pyserial 2.5 (http://pypi.python.org/pypi/pyserial)
"""

import sys
import os
import time
import serial

# create target file
print os.getcwd()
f = open('hardcopy.png', 'wb')

# configure the serial connection
ser = serial.Serial()
ser.port = 0
ser.timeout = 0
ser.baudrate = 9600

ser.open()

# configure the hardcopy settings
cmd = ':HARDCOPY:FORMAT PNG;PALETTE NORMAL;PORT RS232;LAYOUT PORTRAIT;\
PREVIEW 0;INKSAVER 0;COMPRESSION 0\n'
a = ser.write(cmd)
print "bytes sent: {:d}".format(a)

# start hardcopy
a = ser.write("HARDCOPY START\n")
print "bytes sent: {:d}".format(a)

time.sleep(1)

# begin receiving data and writing to file
total_bytes = 0;
a = ser.inWaiting()
while a>0:
    time.sleep(0.5)
    data = ser.read(a)
    total_bytes += a
    f.write(data)
    time.sleep(0.5)
    a = ser.inWaiting()
    sys.stdout.write(".")

# close file and serial port
sys.stdout.write("\n")
f.close()
ser.close()

print "bytes read: {:d}".format(total_bytes)
print "script completed"
