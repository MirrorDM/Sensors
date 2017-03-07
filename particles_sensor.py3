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
    Check Number = sum(00 - 29) (as bytes)
    =========================================================
    |  00  |  01  |  02  |  03  |  04  |  05  |  06  |  07  |
    ---------------------------------------------------------
    | 0x42 | 0x4d | FrameLength | PM1.0  CF=1 | PM2.5  CF=1 |
    =========================================================
    |  08  |  09  |  10  |  11  |  12  |  13  |  14  |  15  |
    ---------------------------------------------------------
    |  PM10 CF=1  |  PM1.0 Air  |  PM2.5 Air  |  PM10  Air  |
    =========================================================
    |  16  |  17  |  18  |  19  |  20  |  21  |  22  |  23  |
    ---------------------------------------------------------
    | 0.3um/0.1L  | 0.5um/0.1L  | 1.0um/0.1L  | 2.5um/0.1L  |
    =========================================================
    |  24  |  25  |  26  |  27  |  28  |  29  |  30  |  31  |
    ---------------------------------------------------------
    | 5.0um/0.1L  |  10um/0.1L  | Ver. | Err. | CheckNumber |
    =========================================================
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
        ver, err, checksum) = struct.unpack('>BB13HBBH', most_recent_data)
        # Check start bytes.
        if sign1 == 0x42 and sign2 == 0x4d and self.check(most_recent_data):
            return (pm1_0_cf, pm2_5_cf, pm10_cf,
                pm1_0, pm2_5, pm10,
                cnt_03, cnt_05, cnt_10,
                cnt_25, cnt_50, cnt_100)
        else:
            return (-1, -1, -1
                -1, -1, -1,
                -1, -1, -1,
                -1, -1, -1)

    def close(self):
        self.serial.close()

    @staticmethod
    def check(data):
        # Checksum = Sum(byte[0], bytes[1], ... bytes[29])
        bytes_data = struct.unpack('>30BH', data)
        return sum(bytes_data[:30]) == bytes_data[-1]


def main():
    sensor = ParticlesSensor()
    while True:
        try:
            (pm1_0_cf, pm2_5_cf, pm10_cf,
                pm1_0, pm2_5, pm10,
                cnt_03, cnt_05, cnt_10,
                cnt_25, cnt_50, cnt_100) = sensor.readPM()
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(now_time)
            print('US PM1.0:', pm1_0_cf)
            print('US PM2.5:', pm2_5_cf)
            print('US PM10 :', pm10_cf)
            print('CN PM1.0:', pm1_0)
            print('CN PM2.5:', pm2_5)
            print('CN PM10 :', pm10)
            print('0.3um/0.1L', cnt_03)
            print('0.5um/0.1L', cnt_05)
            print('1.0um/0.1L', cnt_10)
            print('2.5um/0.1L', cnt_25)
            print('5.0um/0.1L', cnt_50)
            print('10um/0.1L', cnt_100)
            print('--------------------')
            time.sleep(5)
        except KeyboardInterrupt as e:
            print('Keyboard Interrupted. Read Sensor Finished.')
            sensor.close()
            break

if __name__ == '__main__':
    main()