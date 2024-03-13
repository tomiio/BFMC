#!/usr/bin/env python3
import serial
import rospy
import json
import time
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool
from utils.srv import subscribing, subscribingResponse

class AutomatedControlTransmitterProcess():
    #==============================INIT==============================
    def __init__(self):
        
        #init com
        devFile = '/dev/ttyACM0'
        self.serialCom = serial.Serial(devFile, 19200, timeout = 0.1)
        self.serialCom.flushInput()
        self.serialCom.flushOutput()
        
        rospy.init_node('AUTOMATEDnod', anonymous=False) 
        rospy.loginfo("Node has been started!")

        self.kp = 0.12
        self.ki = 0
        self.kd = 0
        self.PID = 0
        self.P = 0 
        self.I = 0 
        self.D = 0 
        self.error = 0
        self.count = 0
        self.lastState = ''
        self.signState = ''
        self.interCount = 0
        self.localState = False
        self.loseSignal = False
        self.preTurn = 0

        self.publisher = rospy.Publisher('/automobile/command', String, queue_size = 1)
        #self.sub = rospy.Subscriber('/automobile/command',String, self.callback_encoder, queue_size = 1)
        #self.local_sub = rospy.Subscriber('/local_message', Float32, self.callback_local)
        #self.local_sub = rospy.Subscriber('/local_message', String, self.callback_local)
        self.xmid_sub = rospy.Subscriber('/middlePoint_data', String, self.callback_xmid, queue_size = 1)
        #self.signs_sub = rospy.Subscriber('/signs_message', String, self.callback_signs)
        self.enc_sub = rospy.Service("command_feedback_en", subscribing, self.enc)


        command = {'action': '1', 'speed': 0.15}
        self.sendCommand(command)
        time.sleep(0.1)
        
        command = {'action': '4', 'activate': False}
        self.sendCommand(command)
        time.sleep(0.3)
        
#         command = {'action': '7', 'distance': 0.5, 'speed': 0.1}
#         self.sendCommand(command)
#         time.sleep(0.3)
            
#         command = {'action': '4', 'activate': True}
#         self.sendCommand(command)
#         time.sleep(0.3)
#         
        command = {'action': '5', 'activate': True}
        self.sendCommand(command)
        time.sleep(0.3)
# 
#         command = {'action': '1', 'speed': 0.1}
#         command = json.dumps(command)
#         self.publisher.publish(command)
# 
#         time.sleep(0.1)

        
#         command = {'action': '1', 'speed': 0.15}
#         self.sendCommand(command)


        print("init")
        rospy.Rate(30)
        rospy.spin()
    #==============================RUN==============================
    def enc(self, msg):
        print(msg)
        
    def looping(self):
        while not rospy.is_shutdown():
#             command = {'action': '1', 'speed': 0.0}
#             self.sendCommand(command)
             time.sleep(0.1)
            
            
#             command = {'action': '7', 'distance': 5, 'speed': 0.1}
#             self.sendCommand(command)
            
    def run(self, data, inter):
#         msg = self.serialCom.read()
#         msg = msg.decode("ascii")
#         print("encoder msg: ", msg)
        
        #while not rospy.is_shutdown():
        #print("running")
            # data = self.callback
            # print(data)
#         if inter == 'True':
#             print("intersection")
#             self.interCount +=1
#         else: self.interCount = 0
#         
#         if self.interCount >= 4:
#             print("intersection detected!!!")
#             if self.signState == 'stop':
#                 command = {'action': '1', 'speed': 0.0}
#                 self.sendCommand(command)
#                 time.sleep(5)
#                 self.signState = ''
#             self.interCount = 0
#             command = {'action': '1', 'speed': 0.2}
#             self.sendCommand(command)
# 
#             command = {'action': '2', 'steerAngle': 0}
#             self.sendCommand(command)
#             time.sleep(2)

            

        
        steer = self.PIDfunction(data)
        #print(steer)
        #if inter != 'True':

#         command = {'action': '1', 'speed': 0.1}
#         command = json.dumps(command)
#         self.publisher.publish(command)

#         command = {'action': '2', 'steerAngle': steer}
#         command = json.dumps(command)
#         self.publisher.publish(command)

    def callback_encoder(self, data):
        print(data)
    
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

    def callback_xmid(self, data):

        data = json.loads(data.data)
        #print(data['x'], ' ', data['intersection'])
        if self.localState == False:
            self.run(data['x'], data['intersection'])

        return data['x'], data['intersection']

    def callback_signs(self, data):
        data = json.loads(data.data)
        print(data['signs'])
        if data['signs'] == 'stop':
            self.fstop()
        elif data['signs'] == 'crosswalk':
            self.fcrosswakk()
        elif data['signs'] == 'pedestrian' or data['signs'] == 'car':
            self.fobstacles(data['x0'],data['y0'],data['x1'],data['y1'])


        self.lastState = data['signs']

    def fstop(self):
        #print(time.time() - self.count)
        if self.lastState == 'stop':
            self.count += 1
        else: self.count = 0

        if self.count >= 10:
            self.signState = 'stop'
            self.count = 0

    def fcrosswakk(self):
        command = {'action': '1', 'speed': 0.1}
        self.sendCommand(command)

    def fobstacles(self,x0,y0,x1,y1):
        if ((180 < x0 < 510) or (180 < x1 < 510)) and ((300 < y0 < 480) or (300 < y1 < 480)):
            print('obstacles detected')
            command = {'action': '1', 'speed': 0.0}
            self.sendCommand(command)


    def roundLeft(self):
        
        command = {'action': '2', 'steerAngle': -21}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': 0.1}
        self.sendCommand(command)

        print("up")
        self.around = False

        time.sleep(2)

        command = {'action': '2', 'steerAngle': 21}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': -0.1}
        self.sendCommand(command)

        print("down")
        self.around = True

        time.sleep(2)

        
    def roundRight(self):
        command = {'action': '2', 'steerAngle': 21}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': 0.1}
        self.sendCommand(command)

        time.sleep(2)

        command = {'action': '2', 'steerAngle': -21}
        self.sendCommand(command)
        time.sleep(0.01)
        command = {'action': '1', 'speed': -0.1}
        self.sendCommand(command)

        time.sleep(2)

    def PIDfunction(self, position):

        self.P = position - 360
        self.I = self.P + self.error
        self.D = self.P - self.error
        self.error = self.P

        self.PID = self.kp*self.P + self.ki*self.I + self.kd*self.D

        if self.PID > 21:
            self.PID = 21
        elif self.PID < -21:
            self.PID = -21
        return self.PID
        
    def sendCommand(self, command):
        command = json.dumps(command)
        self.publisher.publish(command)


if __name__ == '__main__':
    try:
        nod = AutomatedControlTransmitterProcess()
        nod.looping()
        #nod.run()

    except rospy.ROSInterruptException:
        pass