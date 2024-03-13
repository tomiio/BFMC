#!/usr/bin/env python3

import rospy
import json
import time
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool

class taskNODE():
    def __init__(self):
        
        rospy.init_node('taskNODE', anonymous=False) 
        rospy.loginfo("taskNODE has been started!")
        
        # Actuator Variables:
        self.speed = 25
        self.steer = 0
        
        self.pre_speed = self.speed
        self.pre_speed_smooth = 25
        
        
        # PID steer tasks variable:
        self.xmid_data = 320.0
        self.image_center = 320.0
        self.kp = 0.15#0.17
        self.ki = 0.0
        self.kd = 0.0
        self.PID = 0.0
        self.P = 0.0
        self.I = 0.0 
        self.D = 0.0 
        self.error = 0.0
        self.max_steer = 25
        
        
        # Signs task variable
        # 0: 'car', 1: 'crosswalk', 2: 'highway_entry', 3: 'highway_exit', 4: 'no_entry', 5:'onewayroad', 6: 'parking', 7: 'pedestrian', 8: 'priority', 9:'roundabout', 10: 'stop', 11: 'trafficlight'
    
        self.signs = [0,0,0,0,0,0,0,0,0,0,0,0]
        
        # Distance + imu task variable
        self.d1 = 0
        self.d2 = 0
        self.d3 = 0
        self.d4 = 0
        self.d5 = 0
        self.yaw = 0
        
        # Pause status
        self.pause = False
        
        # Publisher
        self.publisher = rospy.Publisher('/automobile/command', String, queue_size = 1)
        
        # Subscriber
        self.middlePoint_sub = rospy.Subscriber('/middlePoint_data', String, self.xmid_callback, queue_size = 1)
        self.signs_sub = rospy.Subscriber('/automobile/signs_task', String, self.signs_callback, queue_size = 1)
        self.distance_sub = rospy.Subscriber('/automobile/distance_data', String, self.distance_callback, queue_size = 1)
        self.imu_sub = rospy.Subscriber('/automobile/imu_data', String, self.imu_callback, queue_size = 1)
        
        # self.intersection_sub = rospy.Subscriber('/automobile/intersection', String, self.inter_sub, queue_size = 1)
        # self.position_sub = rospy.Subscriber('/automobile/position', String, self.pos_sub, queue_size = 1)
        
        
        # rospy.spin()
        
    ############## CALLBACK ###############
        
    def xmid_callback(self, data):
        data = json.loads(data.data)
        self.xmid_data = data['x']
        # self.steer = self.PIDfunction(data['x']) # Set PID steering
        
    
    def signs_callback(self, data):
        data = json.loads(data.data)
        self.signs = data['list_task']
        
    
    def distance_callback(self, data):
        data = json.loads(data.data)
        self.d1 = data['d1']
        self.d2 = data['d2']
        self.d3 = data['d3']
        self.d4 = data['d4']
        self.d5 = data['d5']
        
        if float(self.d3) <= 25.0 and self.pause == False:
            self.pre_speed = self.speed
            self.speed = 0
            self.pause = True
        elif (float(self.d3) > 25.0) and (self.pause == True):
            # print(self.pre_speed)
            self.speed = self.pre_speed
            self.sendCommand(self.speed, self.steer)
            self.pause = False        
        
        # print(self.distance)
        
    
    def imu_callback(self, data):
        data = json.loads(data.data)
        self.yaw = float(data['yaw'])
        
    
    ############## PROCESS #############
    
    def main_process(self):
        while not rospy.is_shutdown():
            # print("processing")
            # 1
            # Xu ly steering
            # print(1)
            self.steer = self.PIDfunction(self.xmid_data) # Set PID steering
            
            # 2
            # Xu ly tung sign
            # 0: 'car', 1: 'crosswalk', 2: 'highway_entry', 3: 'highway_exit', 4: 'no_entry', 5:'onewayroad', 
            # 6: 'parking', 7: 'pedestrian', 8: 'priority', 9:'roundabout', 10: 'stop', 11: 'trafficlight'
            # print(2)
            
            if self.signs[5] == 1:      # one way road -- DO NOTHING
                print("one way road")
                self.signs[5] = 0
                pass
            
            if self.signs[4] == 1:      # no entry -- DO NOTHING
                print("no entry")
                self.signs[4] = 0
                pass
            
            if self.signs[9] == 1:      # round about
                print("round about")
                self.signs[9] = 0
                pass
                
            if self.signs[2] == 1:      # highway entry -- DONE
                print("highway entry")
                self.f_highwayEntry()
                self.signs[2] = 0
                pass
                
                
            if self.signs[3] == 1:      # highway exit -- DONE
                print("highway exit")
                self.f_highwayExit()
                self.signs[3] = 0
                pass
            
            if self.signs[1] == 1:      # cross walk -- DONE
                print("cross walk")
                self.f_crosswalk()
                self.signs[1] = 0
                pass       
            
            if self.signs[6] == 1:      # parking -- DONE
                print("parking")
                self.f_parking()
                self.signs[6] = 0   
                pass      

            if self.signs[11] == 1:     # traffic light
                print("traffic light")
                self.signs[11] = 0 
                pass 
            
            if self.signs[10] == 1:     # stop -- WORKING
                print("stop")
                self.f_stop()
                self.signs[10] = 0 
                pass    
            
            if self.signs[0] == 1:      # car -- WORKING
                print("car")
                self.signs[0] = 0 
                pass                       
            
            if self.signs[7] == 1:      # pedestrian -- WORKING
                print("pedestrian")
                self.signs[7] = 0 
                pass      
            
            
            # # 3
            # # Xu ly vat can, Combine distance sensor + heading -> Ne vat can
            # # print(self.distance)
            # if float(self.d3) <= 30.0:
            #     self.speed = 0
            # else:
            #     self.speed = 25
            
            if float(self.d2) <= 10.0:
                self.steer = 25
            
            if float(self.d4) <= 10.0:
                self.steer = -25  
            # print(3)
            
            
            
            # END of each loop
            self.sendCommand(self.speed, self.steer) #speed, steer
            # time.sleep(0.01)
            # print(4)
            # self.sendCommand(0, 0)
        
    
    ################# Related Function #################
    
    
    def PIDfunction(self, position):

        self.P = position - self.image_center
        self.I = self.P + self.error
        self.D = self.P - self.error
        self.error = self.P

        self.PID = self.kp*self.P + self.ki*self.I + self.kd*self.D
        #print('STEERRRRRR:', self.PID)
        if self.PID > self.max_steer:
            self.PID = self.max_steer
        elif self.PID < -self.max_steer:
            self.PID = -self.max_steer
        
        return self.PID
    
    def sendCommand(self, speed, steer):
        
        if self.pre_speed_smooth != speed:
            if speed > self.pre_speed_smooth:
                while speed - self.pre_speed_smooth > 0:
                    self.pre_speed_smooth += 1
                    command = {'action': '1', 'speed': float(self.pre_speed_smooth)}
                    command = json.dumps(command)
                    self.publisher.publish(command)
                    time.sleep(0.01)
            elif speed < self.pre_speed_smooth:
                while self.pre_speed_smooth - speed > 0:
                    self.pre_speed_smooth -= 1
                    command = {'action': '1', 'speed': float(self.pre_speed_smooth)}
                    command = json.dumps(command)
                    self.publisher.publish(command)
                    time.sleep(0.01)                    
                    
        else:
            command = {'action': '1', 'speed': float(speed)}
            command = json.dumps(command)
            self.publisher.publish(command)
            time.sleep(0.01)
        
        command = {'action': '2', 'steerAngle': float(steer)}
        command = json.dumps(command)
        self.publisher.publish(command)
        time.sleep(0.01)
        
        self.pre_speed_smooth = self.speed
        
    # Xu ly tung sign
    # 0: 'car', 1: 'crosswalk', 2: 'highway_entry', 3: 'highway_exit', 4: 'no_entry', 5:'onewayroad', 
    # 6: 'parking', 7: 'pedestrian', 8: 'priority', 9:'roundabout', 10: 'stop', 11: 'trafficlight'
    
    def timepause(self,t):
        start_time = time.time()
        time_lost = 0
        while (time.time() - start_time) < t:
            # print(t)
            time.sleep(0.1)
            time_lost = 0
            while self.pause == True:
                print("Pause due to Obstacle")
                self.sendCommand(0,self.steer)
                time.sleep(0.1)
                time_lost += 0.1
            t += time_lost
            
    
    
    def f_highwayEntry(self):
        self.speed = 27
        pass
    
    def f_highwayExit(self):
        self.speed = 25
        pass
            
    def f_crosswalk(self):
        self.speed = 10
        self.sendCommand(self.speed,self.steer)
        self.timepause(10)
        self.speed = 25
        self.sendCommand(self.speed,self.steer)
        self.timepause(0.1)
        pass
            
    def f_car(self):
        pass
    
    def f_pedestrian(self):
        pass
                
            
    def f_stop(self):
        print("STOP!!!")
        # self.speed = 0
        # self.steer = 0
        self.sendCommand(0, self.steer)
        self.timepause(3)
        self.sendCommand(25, self.steer)
    
    
    def f_parking(self):
        print("start parking")
        # go straight ahead
        self.speed = 20
        self.steer = 0
        
        # self.sendCommand(self.speed, self.steer)
        # self.timepause(5)
        
        for i in range(50):
            self.straight_parking(self.speed, 0.1)
            
        
        # check if empty
        print("Checking empty slot!!!")
        self.speed = 0
        self.steer = 0
        self.sendCommand(self.speed, self.steer)
        self.timepause(2)
        
        print("Checking empty slot found!!!")
        
        # start parallel parking
        self.speed = 20
        # self.steer = 5
        self.straight(self.speed, 5) # [speed, time] 
        
        self.speed = 0
        self.steer = 0
        self.sendCommand(0,0)
        self.timepause(1)
        
        self.speed = 20
        self.steer = 25
        self.rightBackwardCurve(self.speed, self.steer, 2.5) # [speed, steer, t]
        
        self.speed = 20
        self.steer = 25
        self.leftBackwardCurve(self.speed, self.steer, 3)
        
        self.speed = 0
        self.straight(self.speed, 0.1)
        
        self.timepause(3)
        print("end parking")
        pass
    
    ############################### blind Control #################################
    def rightFowardCurve(self, speed, steer_angle, t):
        self.sendCommand(speed, steer_angle)
        self.timepause(t)     
        # Back to straight direction
        # self.sendCommand(0,0)
        
            
    def rightBackwardCurve(self, speed, steer_angle, t):
        self.sendCommand(-speed, steer_angle)
        self.timepause(t)                   
        # Back to straight direction
        # self.sendCommand(0,0)
            
            
    def leftFowardCurve(self, speed, steer_angle,  t):
        self.sendCommand(speed,-steer_angle)
        self.timepause(t)            
        # Back to straight direction
        # self.sendCommand(0,0)
        
            
    def leftBackwardCurve(self, speed, steer_angle, t):
        self.sendCommand(-speed,-steer_angle)
        self.timepause(t)        
        # Back to straight direction
        # self.sendCommand(0,0)
        
            
    def straight(self, speed, t):
        self.sendCommand(speed,0)
        self.timepause(t)           
        # Stop before doing any tasks
        # self.sendCommand(0,0)
    
    def straight_parking(self, speed, t):
        # self.sendCommand(speed,0)
        self.steer = self.PIDfunction(self.xmid_data)
        self.sendCommand(speed, self.steer)
        self.timepause(t)           
        # Stop before doing any tasks
        # self.sendCommand(0,0)   
        
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
        self.rightFowardCurve(20, 20, 6) # [speed, steer, time]
        # self.straight(20, 1.5)
        # self.rightFowardCurve(20, 25, 2) # [speed, steer, time]
        self.straight(20, 0.1)
    
    
    def roundAboutStraigt(self):
        self.straight(20, 2)
        self.rightFowardCurve(20, 20, 4) # [speed, steer, time]
        self.leftFowardCurve(20, 20, 4)
        self.rightFowardCurve(20, 20, 4)
        self.straight(20, 2)
        

    def roundAboutLeft(self):
        self.straight(20, 2) # [speed, time] 
        self.rightFowardCurve(20, 20, 4) # [speed, steer, time]
        self.leftFowardCurve(20, 20, 10)
        self.rightFowardCurve(20, 20, 4)
        self.straight(20, 2)

    
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
        
        
                
if __name__ == "__main__":
    try:
        nod = taskNODE()
        nod.main_process()

    
    except rospy.ROSInterruptException:
        pass