#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

class fakeActionNode:
    def __init__(self):
        rospy.init_node('fakeActionNODE', anonymous=False)
        self.pub = rospy.Publisher('/automobile/fakeaction', String, queue_size=1)
        
    def run(self):
        while not rospy.is_shutdown():
            action = input("Input action: ")
            self.pub.publish(action)

            
if __name__ == '__main__':
    fakeAction = fakeActionNode()
    fakeAction.run()