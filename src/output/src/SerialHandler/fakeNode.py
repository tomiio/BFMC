
import serial
from messageconverter import MessageConverter
import json

import time
def serialFunc():
    devFile = '/dev/ttyACM0'
    
    serialCom = serial.Serial(devFile, 19200)

    time.sleep(1)
    serialCom.write("#1:0.000000;;\r\n".encode("ascii"))
    time.sleep(1)
    # serialCom.write("#2:-20.00;;\r\n".encode("ascii"))
    while True:
        
        print("///")
        print()
        serialCom.write("#2:0.00;;\r\n".encode("ascii"))
        time.sleep(0.01)
        serialCom.write("#2:0.00;;\r\n".encode("ascii"))
        time.sleep(0.01)
        
serialFunc()
        