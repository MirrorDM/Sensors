# Sensor Reader

Read SenseAir&reg; S8-0053 from COM Port.

## Installation
#### Python3
Download and install [*Python3*](https://www.python.org/downloads/).

#### pySerial
This module encapsulates the access for the serial port.
    
    pip install pyserial

## Usage
#### Windows
    python.exe co2_sensor.py3
#### Linux / OSX
    python3 co2_sensor.py3

#### Example
    PS C:\Users\Mirror\Desktop> python.exe .\co2_sensor.py3
    
     ------Select COM Port------
     
       [0] Intel(R) Active Management Technology - SOL (COM3)
       [1] 通信端口 (COM1)
       [2] USB-SERIAL CH340 (COM4)
       
     ------Select COM Port------
    
    Select CO2 Sensor, usually contains `CH340': 2
    2017-03-06 19:37:52 CO2(ppm): 844
    2017-03-06 19:37:57 CO2(ppm): 844
    2017-03-06 19:38:02 CO2(ppm): 843
    2017-03-06 19:38:07 CO2(ppm): 844
    2017-03-06 19:38:12 CO2(ppm): 847
    2017-03-06 19:38:17 CO2(ppm): 849
    2017-03-06 19:38:22 CO2(ppm): 854
    ^C
    Keyboard Interrupted. Read Sensor Finished.
