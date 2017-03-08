#!/usr/bin/env python3
'''
    File name: simple_database.py
    Author: MirrorDM
    Date created: 03/08/2017
    Date last modified: 03/08/2017
    Python Version: 3.5
'''
import sqlite3
import time

class SimpleDatabase:

    '''
    TIME_STAMP: from int(time.time())
    '''
    db_file = 'air.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        # List tables.
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_list = set(self.cursor.fetchall())
        # Create table if not exist.
        for res_tuple in table_list:
            if 'Air' not in res_tuple:
                self.cursor.execute("""CREATE TABLE Air
                    (TIME_STAMP BIGINT PRIMARY KEY  NOT NULL,
                    CO2 INT,
                    PM25_US INT,
                    PM25_CN INT,
                    PM100_US INT,
                    PM100_CN INT);""")
                self.conn.commit()

    def insert_data(self, timestamp, co2=None,
        pm25_us=None, pm25_cn=None,
        pm100_us=None, pm100_cn=None):
        self.cursor.execute("""INSERT INTO Air VALUES (?,?,?,?,?,?);""",
            (timestamp, co2, pm25_us, pm25_cn, pm100_us, pm100_cn))
        self.conn.commit()

    def select_data(self, starttime=0, endtime=None):
        if endtime is None:
            endtime = int(time.time())
        self.cursor.execute("""SELECT TIME_STAMP, CO2, 
            PM25_US, PM25_CN, PM100_US, PM100_CN
            FROM Air
            WHERE TIME_STAMP>? AND TIME_STAMP<?""",
            (starttime, endtime))
        data = self.cursor.fetchall()
        return data

    def close(self):
        self.conn.commit()
        self.conn.close()
