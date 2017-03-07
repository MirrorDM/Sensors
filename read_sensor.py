#!/usr/bin/env python3
'''
    File name: read_sensor.py
    Author: MirrorDM
    Date created: 03/08/2017
    Date last modified: 03/08/2017
    Python Version: 3.5
'''
from co2_sensor import CO2Sensor
from particles_sensor import ParticlesSensor
import time
import sqlite3

class SensorReader:

    interval = 5

    def __init__(self):
        self.co2_sensor = CO2Sensor()
        self.particles_sensor = ParticlesSensor()

    def get_time(self):
        self.now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def read_data(self):
        # Read CO2 sensor
        self.co2_ppm = self.co2_sensor.readPPM()
        # Read particles sensor
        (self.pm1_0_us, self.pm2_5_us, self.pm10_us,
        self.pm1_0_cn, self.pm2_5_cn, self.pm10_cn,
        self.cnt_03, self.cnt_05, self.cnt_10,
        self.cnt_25, self.cnt_50, self.cnt_100) = self.particles_sensor.readPM()

    def run_once(self):
        # Get data
        self.read_data()
        self.get_time()
        # Display data
        self.display()
        # Write to database
        self.write_database()

    def write_database(self):
        # TODO
        pass

    def display(self):
        print('---'+self.now_time+'---')
        print('CO2     :', self.co2_ppm)
        print('PM2.5 US:', self.pm2_5_us)
        print('PM10  US:', self.pm10_us)
        print('PM2.5 CN:', self.pm2_5_cn)
        print('PM10  CN:', self.pm10_cn)

    def run(self):
        while True:
            try:
                self.run_once()
                time.sleep(self.interval)
            except KeyboardInterrupt as e:
                print('Keyboard Interrupted. Read Sensor Finished.')
                self.co2_sensor.close()
                self.particles_sensor.close()
                break

def main():
    reader = SensorReader()
    reader.run()

if __name__ == '__main__':
    main()