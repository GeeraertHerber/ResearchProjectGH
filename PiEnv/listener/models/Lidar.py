#!/usr/bin/env python
from time import sleep
import serial


class Lidar:
    def __init__(self,par_serial_port="/dev/serial0", par_baudrate=115200, par_timeout=1):
        self.serial_port = par_serial_port
        self.baudrate = par_baudrate
        self.timeout = par_timeout
        self.serial = None

    def connect_lidar(self):
        self.serial = serial.Serial(self.serial_port, self.baudrate, timeout = self.timeout)

    def read_lidar(self):
        while True: 
            if self.serial.in_waiting > 0:
                output = self.serial.readline(9)
                try:
                    output = {"range":output[2]+output[3]*256, "strength":output[4]+output[5]*256}
                    return output
                except IndexError as e:
                    return None

if __name__ == "__main__":
    lidar = Lidar()
    lidar.connect_lidar()
    while True: 
        print(lidar.read_lidar())
                
