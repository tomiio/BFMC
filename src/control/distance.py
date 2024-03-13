#!/usr/bin/env python3
import serial
import rospy
import json
import time
from std_msgs.msg import String

class distance():
    def __init__(self):
        rospy.init_node('DISTANCEnod', anonymous=False) 
        rospy.loginfo("distance node has been started!")
        
        self.ser = serial.Serial('/dev/ttyACM1', 9600, timeout = 0.1)
        #self.ser = serial.Serial('/dev/ttyS0', 9600)
        self.ser.reset_input_buffer()
        
        self.pub = rospy.Publisher('/distance', String, queue_size = 1)
        
    def run(self):
        #print(0)
        #with open("/dev/ttyACM1","r") as readBuff:

        while not rospy.is_shutdown():
            #print(1)
            #print(readBuff.readline())#.decode('utf-8').rstrip())
#             line = self.ser.readline().decode('utf-8').rstrip()
#             print(line)
            if self.ser.in_waiting > 0:
                #print(2)
                try:
                    line = self.ser.readline().decode('utf-8').rstrip()
    #                 line = line.split(',')
    #                 line = list(map(int, line))
                    print(line)
                    self.pub.publish(line)
                except:
                    pass
                
if __name__ == '__main__':
    try:
        nod = distance()
        nod.run()
    except rospy.ROSInterruptException:
        pass
        
