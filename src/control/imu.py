#!/usr/bin/env python

import rospy
from utils.msg import IMU

class imuThread():
    def __init__(self):
        rospy.init_node('imuDisplayNode',anonymous = True)
        print('init')
        self.imu_sub = rospy.Subscriber('/automobile/IMU', IMU,self.imu_callback, queue_size = 1,buff_size=2**24)
        print('callback')
        rospy.spin()
        
    def imu_callback(self, data):
        print(data)
        print('---')
        
if __name__ == '__main__':
    try:
        nod = imuThread()
    except rospy.ROSInterruptException:
        pass
