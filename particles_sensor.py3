#!/usr/bin/env python3
'''
    File name: pm_sensor.py3
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
import io
import struct

class ParticlesSensor:
    '''
    Active transmission.
    32 bytes. Big-endian.
    Check Number = sum(00 - 29)
    =============================
    |  00  |  01  |  02  |  03  |
    -----------------------------
    | 0x42 | 0x4d | FrameLength |
    =============================
    |  04  |  05  |  06  |  07  |
    -----------------------------
    | PM1.0  CF=1 | PM2.5  CF=1 |
    =============================
    |  08  |  09  |  10  |  11  |
    -----------------------------
    |  PM10 CF=1  |  PM1.0 Air  |
    =============================
    |  12  |  13  |  14  |  15  |
    -----------------------------
    |  PM2.5 Air  |  PM10  Air  |
    =============================
    |  16  |  17  |  18  |  19  |
    -----------------------------
    | 0.3um/0.1L  | 0.5um/0.1L  |
    =============================
    |  20  |  21  |  22  |  23  |
    -----------------------------
    | 1.0um/0.1L  | 2.5um/0.1L  |
    =============================
    |  24  |  25  |  26  |  27  |
    -----------------------------
    | 5.0um/0.1L  |  10um/0.1L  |
    =============================
    |  28  |  29  |  30  |  31  |
    -----------------------------
    | Ver. | Err. | CheckNumber |
    =============================
    '''

    baudrate = 9600
    timeout = None

    def __init__(self):

        # List COM Ports.
        serial_devices = serial.tools.list_ports.comports()
        print('\n ------Select COM Port------\n')
        for num, dev in enumerate(serial_devices):
            print('   ['+str(num)+']', dev.description, dev.device)
        print('\n ------Select COM Port------\n')
        # Select PM Sensor Port.
        selected_num = input('Select PM Sensor, usually contains `CH340\' or `USB-Serial\': ')
        selected_num = int(selected_num)
        if selected_num >= len(serial_devices):
            print('Error device.')
            sys.exit(1)
        # Init serial device.
        self.port = serial_devices[selected_num].device
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def readPM(self):
        all_data = self.serial.read_all()
        if len(all_data) >= 32:
            most_recent_data = all_data[-32:]
        else:
            most_recent_data = self.serial.read(32)
        (sign1, sign2, frame_length,
        pm1_0_cf, pm2_5_cf, pm10_cf,
        pm1_0, pm2_5, pm10,
        cnt_03, cnt_05, cnt_10,
        cnt_25, cnt_50, cnt_100,
        ver, err, checksum) = struct.unpack(">BBHHHHHHHHHHHHHBBH", most_recent_data)

        if sign1 == 0x42 and sign2 == 0x4d:
            return (pm1_0, pm2_5, pm10)
        else:
            return (-1, -1, -1)

    def close(self):
        self.serial.close()

sensor = ParticlesSensor()

while True:
    try:
        (pm1_0, pm2_5, pm10) = sensor.readPM()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(now_time)
        print('PM1.0:', pm1_0)
        print('PM2.5:', pm2_5)
        print('PM10 :', pm10)
        time.sleep(1)
    except KeyboardInterrupt as e:
        print('Keyboard Interrupted. Read Sensor Finished.')
        sensor.close()
        break
