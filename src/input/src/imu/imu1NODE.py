#!/usr/bin/env python3

import json
import time
import math
import rospy
from std_msgs.msg import String

class IMUNode:
    def __init__(self):
        
        self.X = 0
        self.Y = 0
        self.speed = 0
        self.yaw = 0
        self.yaw_rad = 0
        self.current_time = 0
        self.pre_time = 0
        
        
        rospy.init_node('imuNODE', anonymous=False)
        self.command_subscriber = rospy.Subscriber("/automobile/command", String, self.callback_getSpeed)
        self.imu_data = rospy.Subscriber("/automobile/imu_data", String, self.callback_getYaw) 
        self.publisher = rospy.Publisher("/automobile/position", String, queue_size=1)
        
        rospy.spin()
    
    
    def callback_getSpeed(self, data):
        data = json.loads(data.data)
        try:
            self.speed = data['speed']
            # self.current_time = time.time()
        except:
            pass
    
    def callback_getYaw(self, data):
        data = json.loads(data.data)
        self.yaw = float(data['yaw'])
        self.yaw_rad = math.radians(self.yaw)
        self.current_time = time.time()
        
        # Calculate positon
        timestep = self.current_time - self.pre_time
        delta_x = self.speed * math.cos(self.yaw_rad)*timestep
        delta_y = self.speed * math.sin(self.yaw_rad)*timestep
        
        self.pre_time = self.current_time
        
        # Update position
        self.X += delta_x
        self.Y += delta_y
        
        print('X: ', self.X, 'Y: ', self.Y, 'yaw: ', self.yaw)
        
        position_msg = {'x': self.X, 'y': self.Y, 'yaw': self.yaw}
        position_msg = json.dumps(position_msg)
        self.publisher.publish(position_msg)        
        
        pass
    
    # def run(self):
    #     timestep = self.current_time - self.pre_time
    #     delta_x = self.speed * math.cos(self.yaw_rad)*timestep
    #     delta_y = self.speed * math.sin(self.yaw_rad)*timestep
    #     self.pre_time = self.current_time
        
    #     # Update position
    #     self.X += delta_x
    #     self.Y += delta_y
        
    #     print('X: ', self.X, 'Y: ', self.Y)
        
    #     position_msg = {'x': self.X, 'y': self.Y, 'yaw': self.yaw}
    #     position_msg = json.dumps(position_msg)
    #     self.publisher.publish(position_msg)
    #     pass

    
if __name__ == '__main__':
    try:
        nod = IMUNode()
        # nod.run()

    except rospy.ROSInterruptException:
        pass
