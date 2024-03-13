#!/usr/bin/env python3

import rospy
import json
import time
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool

class IntersectionNODE():
    def __init__(self):
        
        rospy.init_node('IntersectionNODE', anonymous=False) 
        rospy.loginfo("IntersectionNODE has been started!")
    
        self.count_intersection = []
        self.num_count = 30
        self.check_intersection = True
        self.threshold_intersection = 0.8
        self.num_reset = 0
        
        self.xmid_sub = rospy.Subscriber('/middlePoint_data', String, self.callback, queue_size=1)
        self.publisher = rospy.Publisher('/automobile/intersection', String, queue_size = 1)

        
        rospy.spin()
    
    def callback(self, msg):
        
        data = json.loads(msg.data)
        intersection = data['intersection']
        self.count_intersection.append(intersection)
        # print(count_intersection)
        
        if len(self.count_intersection) == self.num_count:
            nums_inter = self.count_intersection.count(1)
            
            if nums_inter/self.num_count > self.threshold_intersection and self.check_intersection:
                
                self.publisher.publish("True")
                self.check_intersection = False
                self.count_intersection = self.count_intersection[len(self.count_intersection)//2:]

            elif nums_inter/self.num_count == self.num_reset:
                self.check_intersection = True
                self.count_intersection.pop(0)
            else:
                self.count_intersection.pop(0)
                
if __name__ == "__main__":
    IntersectionNODE()