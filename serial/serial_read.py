#!/usr/bin/env python
import time
import serial
for y in range(15):
    with  serial.Serial(port='/dev/ttyS0', timeout = 15) as ser:
        x = str(ser.readline())
        x = x.split('$')
        print(x)
