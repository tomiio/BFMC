#!/usr/bin/env python3

import serial
import rospy
import json
import time
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool


class AutomatedControlTransmitterProcess():
    #==============================INIT==============================
    def __init__(self):
        rospy.init_node('AUTOMATEDnod', anonymous=False) 
        rospy.loginfo("Node has been started!")

        self.once = 1

        self.kp = 0.17
        self.ki = 0.0
        self.kd = 0
        self.PID = 0.0
        self.P = 0.0
        self.I = 0.0 
        self.D = 0.0 
        self.error = 0.0

        self.steer = 0.0
        self.speed = 0.2

        self.count = 0
        self.lastState = ''
        self.signState = ''
        self.interCount = 0
        self.localState = False
        self.preTurn = 0
        self.overtake = ''
        self.overtakingState = 0 #0 - False; 1 - True left; 2 - True right
        self.dis = [] # 0 left; 1 right; 2 front
        
        self.sleep = False
        self.order = 1

        self.publisher = rospy.Publisher('/automobile/command', String, queue_size = 1)
        #self.local_sub = rospy.Subscriber('/local_message', String, self.callback_local)
        self.xmid_sub = rospy.Subscriber('/middlePoint_data', String, self.callback_xmid)
        #self.dis_sub = rospy.Subscriber('/distance', String, self.callback_dis)
        #self.signs_sub = rospy.Subscriber('/signs_message', String, self.callback_signs)
        self.check_sub = rospy.Subscriber('/check', Bool, self.callback_main)


        print("init")
        rospy.spin()

    def callback_xmid(self, data):
        #if self.order == 1:
        print("---xmid---")
        if self.sleep == False:

            data = json.loads(data.data)
            self.overtake = data['pass']
            #print(data['x'], ' ', data['intersection'])
            if self.localState == False:
                if data['intersection'] == 'True':
                    #print("intersection")
                    self.interCount +=1
                else: self.interCount = 0

            if self.interCount >= 4:
                #print("intersection detected!!!")
                if self.signState == 'stop':
                    command = {'action': '1', 'speed': 0.0}
                    self.sendCommand(command)
                    time.sleep(5)
                    self.signState = ''
                    self.interCount = 0
                
            self.steer = self.PIDfunction(data['x'])
            print(self.steer)
            if data['intersection'] != 'True':

                self.steer = self.PIDfunction(data['x'])
                print(self.steer)

            # command = {'action': '1', 'speed': 0.3}
            # command = json.dumps(command)
            # self.publisher.publish(command)
            # time.sleep(0.1)

            # command = {'action': '2', 'steerAngle': self.steer}
            # command = json.dumps(command)
            # self.publisher.publish(command)

            #self.run(data['x'], data['intersection'], data['pass'])
        self.order = 2
     

    def callback_local(self, data):
        #print(data.data)

        command = {'action': '1', 'speed': 0.2}
        self.sendCommand(command)
        time.sleep(0.1)

        if data.data == 'TurnLeft':
            if self.preTurn == 'KeepMoving':
                time.sleep(6)

            command = {'action': '2', 'steerAngle': -16}
            self.localState = True
            self.sendCommand(command)
            print("turningLeft")
                
        elif data.data == 'TurnRight':
            if self.preTurn == 'KeepMoving':
                time.sleep(6)

            command = {'action': '2', 'steerAngle': 21}
            self.localState = True
            self.sendCommand(command)
            print("turningRight")

        elif data.data == 'Straight':
            if self.preTurn == 'KeepMoving':
                time.sleep(6)

            command = {'action': '2', 'steerAngle': 0}
            self.localState = True
            self.sendCommand(command)
            print("Going Ahead")
        else:
            if self.preTurn == 'TurnRight':
                #time.sleep(1)
                for i in range(8):
                    self.roundRight()

            self.localState = False
            print("PID move")
        
        self.preTurn = data.data

        # if data.data == 0:
        #     self.localState = True
        # elif data.data == 21:
        #     self.localState = False
        #     self.roundRight()
        # elif data.data == -21:
        #     self.localState = False
        #     self.roundLeft()
        # else:
        #     command = {'action': '2', 'steerAngle': data.data}
        #     self.sendCommand(command)

            # self.sendCommand(command)
            # print("turning")
            # time.sleep(10)

        #self.roundLeft()
        #print("round left")
        return data.data


    def callback_signs(self, data):
        #if self.order == 3:
        print("---signs---")
        data = json.loads(data.data)
        print(data['signs'])
        #self.speed = 0.15

        if data['signs'] == 'stop':
            self.fstop()
        elif data['signs'] == 'crosswalk':
            self.fcrosswakk()
        elif data['signs'] == 'pedestrian':
            self.fpedestrian(data['x0'],data['y0'],data['x1'],data['y1'])
        elif (data['signs'] == 'car' and self.dis[2] <= 30) or self.overtakingState != 0:
            self.fcar(data['x0'],data['y0'],data['x1'],data['y1'])
        elif data['signs'] == 'Red' or data['signs'] == 'Green':
            self.ftrafficlight(data['signs'])
        elif data['signs'] == 'highway_entry':
            self.fhighwayentry()
        elif data['signs'] == 'highway_exit':
            self.fhighwayexit()
        elif data['signs'] == 'roadblock':
            self.froadblock()
            

        else:
            self.speed = 0.15

        self.lastState = data['signs']
        self.order = 4 

    def fstop(self):
        if self.lastState == 'stop':
            self.count += 1
        else: self.count = 0

        if self.count >= 10:
            self.signState = 'stop'
            self.count = 0

    def fcrosswakk(self):
        # command = {'action': '1', 'speed': 0.1}
        # self.sendCommand(command)
        self.speed = 0.08

    def fpedestrian(self,x0,y0,x1,y1):
        if ((180 < x0 < 510) or (180 < x1 < 540)) and (200 < y1 < 405):
            print('obstacles detected')
            self.speed = 0.0

    def fcar(self,x0,y0,x1,y1):
        # command = {'action': '1', 'speed': 0.1}
        # self.sendCommand(command)
        if (((180 < x0 < 510) or (180 < x1 < 540)) and (190 < y1 < 480)) and self.dis[2] <= 40:
            print('car detected')
            print('overtake: ', self.overtake)
            #self.overtakingState = 1
            #self.switchlane(self.speed,'left')
            #self.overtakingState = 1
            if self.overtake == 'True_Left':
                self.overtakingState = 1
                self.switchlane(self.speed,'left')
            elif self.overtake == 'True_Right':
                self.overtakingState = 2
                self.switchlane(self.speed,'right')
            else:
                # tailing
                command = {'action': '1', 'speed': 0.0}
                self.sendCommand(command)
                time.sleep(0.01)
        print('overtakeState: ', self.overtakingState)
                
        if self.overtakingState == 1 and self.dis[1] == -1:
            self.switchlane(self.speed, 'right')
            self.overtakingState = 0
        elif self.overtakingState == 2 and self.dis[0] == -1:
            self.switchlane(self.speed, 'left')
            self.overtakingState = 0
            
#         if 'left':
#             command = {'action': '1', 'speed': 0.2}
#             self.sendCommand(command)
#             time.sleep(0.01)
#             command = {'action': '2', 'steerAngle': -23.0}
#             self.sendCommand(command)
#             time.sleep(2.5)
#             command = {'action': '2', 'steerAngle': 23.0}
#             self.sendCommand(command)
#             time.sleep(5)
#             command = {'action': '1', 'speed': 0.0}
#             self.sendCommand(command)
#             time.sleep(0.01)
#             command = {'action': '2', 'steerAngle': 0.0}
#             self.sendCommand(command)
#             time.sleep(0.01)
#             
#         elif 'right':
#             command = {'action': '1', 'speed': 0.2}
#             self.sendCommand(command)
#             time.sleep(0.01)
#             command = {'action': '2', 'steerAngle': 23.0}
#             self.sendCommand(command)
#             time.sleep(2.5)
#             command = {'action': '2', 'steerAngle': -23.0}
#             self.sendCommand(command)
#             time.sleep(5)
#             command = {'action': '1', 'speed': 0.0}
#             self.sendCommand(command)
#             time.sleep(0.01)
#             command = {'action': '2', 'steerAngle': 0.0}
#             self.sendCommand(command)
#             time.sleep(0.01)

            

    def fhighwayentry(self):
        self.speed = 0.2

    def fhighwayexit(self):
        self.speed = 0.15
    
    def fpriority(self):
        pass

    def fonewayroad(self):
        pass
    
    def froadblock(self):
        
        pass

    def ftrafficlight(self, light):
        if light == 'Red':
            # command = {'action': '1', 'speed': 0.0}
            # self.sendCommand(command)
            self.speed = 0.0
        elif light == 'Green':
            # command = {'action': '1', 'speed': 0.2}
            # self.sendCommand(command)
            self.speed = 0.1
    
    def fparking(self, light):
        pass

    def roundLeft(self, v, s, direction):
        if direction == 'up':
            steer = -23
            v = v
        elif direction == 'down':
            steer = 23
            v = -v

        command = {'action': '2', 'steerAngle': steer}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': v}
        self.sendCommand(command)
        self.around = False

        time.sleep(abs(s/v))

        command = {'action': '2', 'steerAngle': -steer}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': -v}
        self.sendCommand(command)
        self.around = True

        time.sleep(abs(s/v))

        
    def roundRight(self, v, s, direction):
        if direction == 'up':
            steer = 23
            v = v
        elif direction == 'down':
            steer = -23
            v = -v

        command = {'action': '2', 'steerAngle': steer}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': v}
        self.sendCommand(command)

        time.sleep(abs(s/v))

        command = {'action': '2', 'steerAngle': -steer}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': -v}
        self.sendCommand(command)

        time.sleep(abs(s/v))
        
    def parallel_parking(self):
        command = {'action': '1', 'speed': 0.1}
        self.sendCommand(command)
        time.sleep(7)
        command = {'action': '1', 'speed': -0.1}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '2', 'steerAngle': 23.0}
        self.sendCommand(command)
        time.sleep(5)
        command = {'action': '2', 'steerAngle': -23.0}
        self.sendCommand(command)
        time.sleep(5)
        command = {'action': '2', 'steerAngle': 0.0}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': 0.1}
        self.sendCommand(command)
        time.sleep(1.5)
        command = {'action': '1', 'speed': 0.0}
        self.sendCommand(command)
        time.sleep(5)

    def switchlane(self,v,direction):
        self.sleep = True
        if direction == "left":
            print("time",0.55/v)
            command = {'action': '2', 'steerAngle': -23.0}
            self.sendCommand(command)
            time.sleep(0.01)
        elif direction == "right":
            command = {'action': '2', 'steerAngle': 23.0}
            self.sendCommand(command)
            time.sleep(0.01)
        command = {'action': '1', 'speed': v}
        self.sendCommand(command)
        
        print("time sleeping: ",0.45/v)
        
        time.sleep(0.45/v)
        
        #rospy.sleep(0.45/v)
        print("end sleeping: ",0.45/v)
        
        if direction == "left":
            command = {'action': '2', 'steerAngle': 23.0}
            self.sendCommand(command)
            time.sleep(0.01)
        elif direction == "right":
            command = {'action': '2', 'steerAngle': -23.0}
            self.sendCommand(command)
            time.sleep(0.01)
        
        self.sleep = True
        time.sleep((0.55/v))
        self.sleep = False
        #rospy.sleep(0.55/v)
        command = {'action': '2', 'steerAngle': 0.0}
        self.sendCommand(command)
        time.sleep(0.01)
        
        # delete command below
        
        command = {'action': '1', 'speed': 0.0}
        self.sendCommand(command)
        time.sleep(0.01)
        self.sleep = False
        

    def PIDfunction(self, position):

        self.P = position - 360.0
        self.I = self.P + self.error
        self.D = self.P - self.error
        self.error = self.P

        self.PID = self.kp*self.P + self.ki*self.I + self.kd*self.D
        #print('STEERRRRRR:', self.PID)
        if self.PID > 23.0:
            self.PID = 23.0
        elif self.PID < -23.0:
            self.PID = -23.0
        return self.PID
        
    def sendCommand(self, command):
        command = json.dumps(command)
        self.publisher.publish(command)
        
    def fled(self,signal):
        file = open('leddata.txt','w')
        signal = 'left'
        file.write(signal)
        file.close()
        
    def callback_dis(self, data):
        #if self.order == 2:
        print("---distance---")
        #print(data.data)
        msg = data.data
        msg = msg.split(',')
        msg = list(map(int, msg))
        self.dis = msg
        print(self.dis)
        self.order = 3
#         if msg[0] <= 15:
#             self.steer = 
        

    def callback_main(self, data):
        #if self.order == 4:
        #print("---main---")
        #------------COMMAND INIT-----------
#         command = {'action': '1', 'speed': 0.0}
#         self.sendCommand(command)
        
        if self.once == 1:
            command = {'action': '4', 'activate': True}
            self.sendCommand(command)
            time.sleep(0.01)
            #self.parallel_parking()

            
            self.once = 0
            #time.sleep(5)
        
        #print(self.serialCom.read())
        #command = {'action': '1', 'speed': 0.0}
        #self.sendCommand(command)
            #self.switchlane(0.2, 'right')


        #-----------------------MAIN----------------------
        #self.fled('right')
            
#
        if self.sleep == False:
            command = {'action': '1', 'speed': self.speed}
            self.sendCommand(command)
            time.sleep(0.01)

            command = {'action': '2', 'steerAngle': self.steer}
            self.sendCommand(command)
            time.sleep(0.01)
        self.order = 1
if __name__ == '__main__':
    try:
        nod = AutomatedControlTransmitterProcess()

    except rospy.ROSInterruptException:
        pass
