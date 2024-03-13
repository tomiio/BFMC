#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import json
import time

class blindControl:
    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.RADIUS_OF_ROUNDABOUT = 45
        self.STEER_ROUNDABOUT = 20
        self.SPEED_ROUNDABOUT = 20
        rospy.init_node('blindControl', anonymous=False)
        self.pub = rospy.Publisher('/automobile/command', String, queue_size = 1)
        self.sub = rospy.Subscriber('/automobile/fakeaction', String, self.callback)
        rospy.spin()
        
    def sendCommand(self, command):
        command = json.dumps(command)
        self.pub.publish(command)
        time.sleep(0.001)
        
    def rightFowardCurve(self, speed, steer_angle, t):
        # Stop before doing any tasks
        time.sleep(0.01)
        command = {'action': '1', 'speed': 0.0}
        self.sendCommand(command)
        
        # Actions
        # time.sleep(0.01)
        command = {'action': '2', 'steerAngle': float(steer_angle)}
        self.sendCommand(command)
        
        # time.sleep(0.01)
        command = {'action': '1', 'speed': float(speed)}
        self.sendCommand(command)

        # Loop until timeout
        t1 = time.time()
        t2 = t1 + t - 1
        while t2 - t1 < t:
            t2 = time.time()
            
        # Back to straight direction
        command = {'action': '2', 'steerAngle': 0.0}
        self.sendCommand(command)
            
    def rightBackwardCurve(self, speed, steer_angle, t):
        # Stop before doing any tasks
        command = {'action': '1', 'speed': 0.0}
        self.sendCommand(command)
        
        # Actions
        time.sleep(0.01)
        command = {'action': '2', 'steerAngle': float(steer_angle)}
        self.sendCommand(command)
        
        time.sleep(0.01)
        command = {'action': '1', 'speed': float(-speed)}
        self.sendCommand(command)

        # Loop until timeout
        t1 = time.time()
        t2 = t1 + t - 1
        
        while t2 - t1 < t:
            t2 = time.time()
            
        # Back to straight direction
        command = {'action': '2', 'steerAngle': 0.0}
        self.sendCommand(command)
            
            
    def leftFowardCurve(self, speed, steer_angle,  t):
        # Stop before doing any tasks
        command = {'action': '1', 'speed': 0.0}
        self.sendCommand(command)
        
        # Actions
        # time.sleep(0.01)
        command = {'action': '2', 'steerAngle': float(-steer_angle)}
        self.sendCommand(command)
        
        # time.sleep(0.01)
        command = {'action': '1', 'speed': float(speed)}
        self.sendCommand(command)
        
        # Loop until timeout
        t1 = time.time()
        t2 = t1 + t - 1
        while t2 - t1 < t:
            t2 = time.time()
            
        # Back to straight direction
        command = {'action': '2', 'steerAngle': 0.0}
        self.sendCommand(command)
            
    def leftBackwardCurve(self, speed, steer_angle, t):
        # Stop before doing any tasks
        command = {'action': '1', 'speed': 0.0}
        self.sendCommand(command)
        
        # Actions 
        time.sleep(0.01)
        command = {'action': '2', 'steerAngle': float(-steer_angle)}
        self.sendCommand(command)
        
        time.sleep(0.01)
        command = {'action': '1', 'speed': float(-speed)}
        self.sendCommand(command)
        
        # Get current time
        t1 = time.time()
        t2 = t1 + t - 1
    
        while t2 - t1 < t:
            t2 = time.time()
        
        # Back to straight direction
        command = {'action': '2', 'steerAngle': 0.0}
        self.sendCommand(command)
            
    def straight(self, speed, t):
        # Stop before doing any tasks
        command = {'action': '1', 'speed': 0.0}
        self.sendCommand(command)
        
        # time.sleep(0.01)
        command = {'action': '2', 'steerAngle': 0.0}
        self.sendCommand(command)
        
        # Carry out action
        # time.sleep(0.01)
        command = {'action': '1', 'speed': float(speed)}
        self.sendCommand(command)
        
        # Get current time
        t1 = time.time()
        t2 = t1 + t - 1
        
        while t2 - t1 < t:
            t2 = time.time()
            
        # Stop before doing any tasks
        command = {'action': '1', 'speed': 0.0}
        self.sendCommand(command)
        
    def threeWaysTurnLeft(self):
        self.straight(20, 4) # Go straight in seconds
        self.leftFowardCurve(20, 25, 4) # Args [speed, steer, time]
        self.straight(20, 0.1)
    
    def threeWaysTurnRight(self):
        self.straight(20, 1) # Go straight in seconds
        self.rightFowardCurve(20, 25, 5.5) # [speed, steer, time]
        self.straight(20, 0.1)
    
    def roundAboutRight(self):
        self.straight(20, 3) # Go straight in seconds
        self.rightFowardCurve(20, self.STEER_ROUNDABOUT, 6) # [speed, steer, time]
        # self.straight(20, 1.5)
        # self.rightFowardCurve(20, 25, 2) # [speed, steer, time]
        self.straight(20, 0.1)
    
    def roundAboutStraigt(self):
        self.straight(20, 2)
        self.rightFowardCurve(self.SPEED_ROUNDABOUT, self.STEER_ROUNDABOUT, 4) # [speed, steer, time]
        self.leftFowardCurve(self.SPEED_ROUNDABOUT, self.STEER_ROUNDABOUT, 4)
        self.rightFowardCurve(self.SPEED_ROUNDABOUT, self.STEER_ROUNDABOUT, 4)
        self.straight(20, 2)

    def roundAboutLeft(self):
        self.straight(20, 2) # [speed, time] 
        self.rightFowardCurve(self.SPEED_ROUNDABOUT, self.STEER_ROUNDABOUT, 4) # [speed, steer, time]
        self.leftFowardCurve(self.SPEED_ROUNDABOUT, self.STEER_ROUNDABOUT, 10)
        self.rightFowardCurve(self.SPEED_ROUNDABOUT, self.STEER_ROUNDABOUT, 4)
        self.straight(20, 2)
        
    def parking(self):
        self.straight(20, 5) # [speed, time] 
        self.rightBackwardCurve(20, 25, 2.5) # [speed, steer, t]
        self.leftBackwardCurve(20, 25, 3)
        self.straight(20, 0.1)

        pass
    
    def passLaneLeft(self):
        self.leftFowardCurve(20, 25, 2.2)
        self.rightFowardCurve(20, 25, 2.5)
        self.straight(20, 0.1)
        pass

    def passLaneRight(self):
        self.rightFowardCurve(20, 25, 2.5)
        self.leftFowardCurve(20, 25, 2)
        self.straight(20, 0.1)
        pass
        
    def callback(self, msg):
        print("///////////")
        print(msg.data)
        if msg.data == "1": 
            self.threeWaysTurnRight()
        elif msg.data == "2": 
            self.threeWaysTurnLeft()
        elif msg.data == "3": 
            self.roundAboutLeft()
        elif msg.data == "4": 
            self.roundAboutRight()
        elif msg.data == "5": 
            self.roundAboutStraigt()
        elif msg.data == "6":
            self.passLaneLeft()
        elif msg.data == "7":
            self.passLaneRight()
        elif msg.data == "8":
            self.parking()
if __name__ == '__main__':
    blindControl(0.26, 0.061)
    