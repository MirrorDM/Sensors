#!/usr/bin/env python3
'''
    File name: co2_sensor.py3
    Author: MirrorDM
    Date created: 03/06/2017
    Date last modified: 03/06/2017
    Python Version: 3.5
'''
from __future__ import print_function
import serial
import serial.tools.list_ports
import time
import sys

class CO2Sensor:
    cmd = bytearray([0xFE, 0x04, 0x00, 0x03, 0x00, 0x01, 0xD5, 0xC5])
    recv = 7
    baudrate = 9600
    timeout = 0.5
    def __init__(self):
        # List COM Ports.
        serial_devices = serial.tools.list_ports.comports()
        print('\n ------Select COM Port------\n')
        for num, dev in enumerate(serial_devices):
            print('   ['+str(num)+']', dev.description, dev.device)
        print('\n ------Select COM Port------\n')
        # Select CO2 Sensor Port.
        selected_num = input('Select CO2 Sensor, usually contains `CH340\' or `USB2.0-Serial\': ')
        selected_num = int(selected_num)
        if selected_num >= len(serial_devices):
            print('Error device.')
            sys.exit(1)
        # Init serial device.
        self.port = serial_devices[selected_num].device
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def readPPM(self):
        self.serial.write(self.cmd)
        output = self.serial.read(self.recv)
        if output[0] == 0xFE and output[1] == 0x04 and output[2] == 0x02:
            ppm = (output[3] << 8) + output[4]
            return ppm
        else:
            return -1

    def close(self):
        self.serial.close()

sensor = CO2Sensor()

while True:
    try:
        ppm = sensor.readPPM()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(now_time, 'CO2(ppm):', ppm)
        time.sleep(5)
    except KeyboardInterrupt as e:
        print('Keyboard Interrupted. Read Sensor Finished.')
        sensor.close()
        break
