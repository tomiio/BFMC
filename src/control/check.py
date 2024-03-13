#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool
import time

class donothing():
    def __init__(self):
        rospy.init_node('CHECKnod', anonymous=False)     
        
        self.rate = rospy.Rate(10)
        
        self.publisher = rospy.Publisher('/check', Bool, queue_size=1)

    def run(self):
        while not rospy.is_shutdown():
            self.publisher.publish(True)
            #self.rate.sleep()
        self.publisher.publish(False)

if __name__ == '__main__':
    try:
        nod = donothing()
        nod.run()

    except rospy.ROSInterruptException:
        pass
