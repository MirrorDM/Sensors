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
import io
import crcmod

class CO2Sensor:
    '''
    Passive transmission.
    Big-endian. (CRC: little-endian.)
    CRC: CRC-16(Modbus).

    Send:
    =========================================================
    |  00  |  01  |  02  |  03  |  04  |  05  |  06  |  07  |
    ---------------------------------------------------------
    | 0xFE | 0x04 |Start Address| NumberOfReg |     CRC     |
    =========================================================

    CO2 read Example:
    =========================================================
    |  00  |  01  |  02  |  03  |  04  |  05  |  06  |  07  |
    ---------------------------------------------------------
    | 0xFE | 0x04 | 0x00 | 0x03 | 0x00 | 0x01 | 0xD5 | 0xC5 |
    =========================================================

    Receive:
    ==================================================
    |  00  |  01  |  02  |  03  |  04  |  05  |  06  |
    --------------------------------------------------
    | 0xFE | 0x04 |Length|   CO2(ppm)  |     CRC     |
    ==================================================
    '''
    cmd = bytearray([0xFE, 0x04, 0x00, 0x03, 0x00, 0x01, 0xD5, 0xC5])
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
        selected_num = input('Select CO2 Sensor, usually contains `CH340\' or `USB-Serial\': ')
        selected_num = int(selected_num)
        if selected_num >= len(serial_devices):
            print('Error device.')
            sys.exit(1)
        # Init serial device.
        self.port = serial_devices[selected_num].device
        self.serial = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)

    def readPPM(self):
        self.serial.write(self.cmd)
        sensor_data = self.serial.read(7)
        addr, func_code, length, co2_ppm, crc_low, crc_high = struct.unpack(">BBBHBB", sensor_data)
        if addr == 0xFE and func_code == 0x04 and length == 0x02 and self.check(sensor_data):
            return co2_ppm
        else:
            return -1

    def close(self):
        self.serial.close()

    @staticmethod
    def check(data):
        # Checksum = crc16(modbus)
        # Only crc-checksum is little-endian.
        # Data length: 7
        crc_modbus = crcmod.predefined.mkCrcFun('modbus')
        calculated_value = crc_modbus(data[:-2])
        actual_value = struct.unpack('<5xH', data)[0]
        return calculated_value == actual_value


def main():
    sensor = CO2Sensor()
    while True:
        try:
            ppm = sensor.readPPM()
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(now_time, 'CO2(ppm):', ppm)
            with io.open('CO2.log', 'a') as f:
                f.write(now_time + ' CO2(ppm): ' + str(ppm) + '\n')
            time.sleep(5)
        except KeyboardInterrupt as e:
            print('Keyboard Interrupted. Read Sensor Finished.')
            sensor.close()
            break

if __name__ == '__main__':
    main()