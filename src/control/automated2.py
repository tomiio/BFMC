#!/usr/bin/env python3

import serial
import rospy
import json
import time
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Bool
import threading

class AutomatedControlTransmitterProcess():
	#==============================INIT==============================
	def __init__(self):
		rospy.init_node('AUTOMATEDnod', anonymous=False) 
		rospy.loginfo("Node has been started!")
		
		self.event = threading.Event()
		self.waitXmid = False
		self.waitSign = False
		self.waitDist = False
		self.waitMain = False

		self.once = 1
		self.defaultSpeed = 0.5

		self.kp = 0.17#0.17
		self.ki = 0.0
		self.kd = 0.0
		self.PID = 0.0
		self.P = 0.0
		self.I = 0.0 
		self.D = 0.0 
		self.error = 0.0

		self.steer = 0.0
		self.speed = self.defaultSpeed
		
		self.passLeft = True
		self.passRight = False
		
		self.parkingState = ''
		#self.parkingDistance = 0

		self.inHighway = False
		self.roadblockRight = False
		self.roadblockLeft = False

		self.pause = False
		self.count = 0
		self.lastState = ''
		self.signState = ''
		self.interCount = 0
		self.localState = False
		self.preTurn = 0
		self.overtake = ''
		self.overtakingState = 0 #0 - False; 1 - True left; 2 - True right
		self.dis = [0,0,0,0,0,0,0,0] # 0 left; 1 right; 2 front
		
		self.sleep = False
		self.order = 4

		self.publisher = rospy.Publisher('/automobile/command', String, queue_size = 1)
		#self.local_sub = rospy.Subscriber('/local_message', String, self.callback_local)
		self.xmid_sub = rospy.Subscriber('/middlePoint_data', String, self.callback_xmid)
		self.dis_sub = rospy.Subscriber('/distance', String, self.callback_dis)
		self.signs_sub = rospy.Subscriber('/signs_message', String, self.callback_signs)
		self.check_sub = rospy.Subscriber('/check', Bool, self.callback_main)


		print("init")
		rospy.spin()

	def callback_xmid(self, data):
		#if self.waitXmid == False:
		#if self.order == 1:
		self.waitXmid = True
	#print("xmid: ", self.order)
	#if self.order == 1:
	#if self.sleep == False:
		#if self.pause == False:
		print("---xmid---")

		data = json.loads(data.data)

		self.steer = self.PIDfunction(data['x'])
		print(self.steer)

		self.order = 4
		self.waitXmid = False

 

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
		print("WAITTTTTTTTTTTTTTTT",self.waitSign)
		print(data.data)
		#if self.pause == False:
		if self.order == 2 and self.pause == False:
			self.waitSign = True
			#print("signs: ", self.order)
			#if self.order == 2:
			#if self.sleep == False:
			print("---signs---")
			#data = json.loads(data.data)
			print(data.data)
			self.signState = data.data
			#pass
			
			#self.speed = 0.15

			if data.data == 'stop':
			    self.pause = True
			    self.fstop()
			    self.pause = False
			elif data.data == 'crosswalk':
			    self.fcrosswakk()
			elif data.data == 'pedestrian':
			    self.fpedestrian()
			elif data.data == 'parallel':
			    self.pause = True
			    #pass
			    print("PARALLEL PARKINGGGGGGGG")

			    command = {'action': '1', 'speed': 0.0}
			    print("PARALLEL PARKINGGGGGGGG")

			    self.sendCommand(command)
			    print("PARALLEL PARKINGGGGGGGG")

			    time.sleep(0.5)                
			    
			    print("1")

			    command = {'action': '1', 'speed': 0.2}
			    self.sendCommand(command)
			    time.sleep(1)
			    print("2")
			    command = {'action': '1', 'speed': 0.0}
			    self.sendCommand(command)
			    time.sleep(0.5)
			    print("p1")
			    if self.dis[6] >= 20:
			        self.fparallel()
			        print("p2")
			    else:
			        command = {'action': '1', 'speed': 0.2}
			        self.sendCommand(command)
			        time.sleep(1)
			        command = {'action': '1', 'speed': 0.0}
			        self.sendCommand(command)
			        time.sleep(0.5)
			        print("p3")
			        if self.dis[6] >= 20:
			            self.fparallel()
			            print("p4")
			        else:
			            command = {'action': '1', 'speed': 0.2}
			            self.sendCommand(command)
			            time.sleep(1)
			            print("p5")
			            
			    self.pause = False
			        
			elif data.data == 'perpendicular':
			    #pass
			    self.pause = True
			    
			    print("PERPENDICULAR PARKINGGGGG")
			    
			    command = {'action': '1', 'speed': 0.0}
			    self.sendCommand(command)
			    time.sleep(0.5)
			    
			    command = {'action': '1', 'speed': 0.2}
			    self.sendCommand(command)
			    time.sleep(1.5)
			    command = {'action': '1', 'speed': 0.0}
			    self.sendCommand(command)
			    time.sleep(0.5)
			    
			    if self.dis[6] == 0 and self.dis[7] == 0:
			        self.fperpendicular()
			    else:
			        command = {'action': '1', 'speed': 0.2}
			        self.sendCommand(command)
			        time.sleep(1.5)
			        command = {'action': '1', 'speed': 0.0}
			        self.sendCommand(command)
			        time.sleep(0.5)
			        if self.dis[6] == 0 and self.dis[7] == 0:
			            self.fperpendicular()
			        else:
			            command = {'action': '1', 'speed': 0.2}
			            self.sendCommand(command)
			            time.sleep(1)
			        
			    self.pause = False
			    
			    # self.fparallel()
			# elif (data.data == 'car' and self.dis[2] <= 30) or self.overtakingState != 0:
			    # self.fcar(data['x0'],data['y0'],data['x1'],data['y1'])
			elif data.data == 'Red' or data.data == 'Green' or data.data == "Yellow":
			    self.ftrafficlight(data.data)
			elif data.data == 'highway_entry':
			    self.fhighwayentry()
			elif data.data == 'highway_exit':
			    self.fhighwayexit()
			elif data.data == 'roadblock_left':
			    if self.dis[3] > 0 and self.dis[3] < 40 and self.dis[4] > 0 and self.dis[4] < 40:
			        self.froadblock_left()
			    
			elif data.data == 'roadblock_right':
			    if self.dis[3] > 0 and self.dis[3] < 40 and self.dis[4] > 0 and self.dis[4] < 40:
			        self.froadblock_right()
			    

			elif self.inHighway == True:
			    self.speed = self.defaultSpeed + 0.1
			else:
			    self.speed = self.defaultSpeed

			self.lastState = data.data
			self.waitSign = False
			self.order = 3

	def fstop(self):
		#self.sleep = True
		command = {'action': '1', 'speed': 0.0}
		self.sendCommand(command)
		command = {'action': '2', 'steerAngle': 0.0}
		self.sendCommand(command)       
		time.sleep(3)
		command = {'action': '1', 'speed': self.speed}
		self.sendCommand(command)
		time.sleep(1)
		#self.sleep = False

	def fcrosswakk(self):
		# command = {'action': '1', 'speed': 0.1}
		# self.sendCommand(command)
		self.speed = 0.1

	def fpedestrian(self):
		self.speed = 0.1

	def fcar(self):
		if (self.dis[3] > 0 and self.dis[3] < 40) or (self.dis[4] > 0 and self.dis[4] < 40):
			pass
			if self.passLeft == True and self.dis[0] == 0 and self.dis[1] == 0 and (self.dis[2] == 0 or self.dis[2] >= 40):
			    self.switchlane(self.speed, "left")
			
			if self.passRight == True and self.dis[6] == 0 and self.dis[7] == 0 and (self.dis[5] == 0 or self.dis[5] >= 40):
			    self.switchlane(self.speed, "right")
			    

			

	def fhighwayentry(self):
		self.inHighway = True
		self.speed = 0.3

	def fhighwayexit(self):
		self.inHighway = False
		self.speed = 0.2
	
	def fpriority(self):
		pass

	def fonewayroad(self):
		pass
	
	def froadblock_left(self):
		if self.passLeft == True and self.dis[0] == 0 and self.dis[1] == 0 and (self.dis[2] == 0 or self.dis[2] >= 40):
			self.switchlane(self.speed, "left")
		
		#pass

	def froadblock_right(self):
		if self.passRight == True and self.dis[6] == 0 and self.dis[7] == 0 and (self.dis[5] == 0 or self.dis[5] >= 40):
			self.switchlane(self.speed, "right")
			
		#pass

	def ftrafficlight(self, light):
		if light == 'Red' or light =="Yellow":
			# command = {'action': '1', 'speed': 0.0}
			# self.sendCommand(command)
			self.speed = 0.0
		elif light == 'Green':
			# command = {'action': '1', 'speed': 0.2}
			# self.sendCommand(command)
			self.speed = self.speedDefault
	
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
		
	def fparallel(self):
		command = {'action': '1', 'speed': 0.1}
		self.sendCommand(command)
		time.sleep(7)
		command = {'action': '1', 'speed': -0.1}
		self.sendCommand(command)
		command = {'action': '2', 'steerAngle': 23.0}
		self.sendCommand(command)
		time.sleep(5)
		command = {'action': '2', 'steerAngle': -23.0}
		self.sendCommand(command)
		time.sleep(5)
		command = {'action': '2', 'steerAngle': 0.0}
		self.sendCommand(command)
		command = {'action': '1', 'speed': 0.1}
		self.sendCommand(command)
		time.sleep(1.5)
		command = {'action': '1', 'speed': 0.0}
		self.sendCommand(command)
		time.sleep(5)
		
	def fperpendicular(self):
		pass

	def switchlane(self,v,direction):
		#self.sleep = True
		if direction == "left":
			print("time",0.55/v)
			command = {'action': '2', 'steerAngle': -23.0}
			self.sendCommand(command)
			#time.sleep(0.01)
		elif direction == "right":
			command = {'action': '2', 'steerAngle': 23.0}
			self.sendCommand(command)
			#time.sleep(0.01)
		command = {'action': '1', 'speed': v}
		self.sendCommand(command)
		
		print("time sleeping: ",0.45/v)
		
		time.sleep(0.45/v)
		
		#rospy.sleep(0.45/v)
		print("end sleeping: ",0.45/v)
		
		if direction == "left":
			command = {'action': '2', 'steerAngle': 23.0}
			self.sendCommand(command)
			#time.sleep(0.01)
		elif direction == "right":
			command = {'action': '2', 'steerAngle': -23.0}
			self.sendCommand(command)
			#time.sleep(0.01)
		
		self.sleep = True
		time.sleep((0.55/v))
		self.sleep = False
		#rospy.sleep(0.55/v)
		command = {'action': '2', 'steerAngle': 0.0}
		self.sendCommand(command)
		#time.sleep(0.01)
		
		# delete command below
		
		command = {'action': '1', 'speed': 0.0}
		self.sendCommand(command)
		time.sleep(0.01)
		#self.sleep = False
			
	def inter_right(self):
			#self.steer = 23.0
		self.pause = True
		command = {'action': '2', 'steerAngle': 23.0}
		self.sendCommand(command)
		time.sleep(2)
		self.pause = False
	def inter_up(self):
		self.pause = True
		command = {'action': '2', 'steerAngle': 0.0}
		self.sendCommand(command)
		time.sleep(3)
		self.pause = False


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
		time.sleep(0.001)
		
	def fled(self,signal):
		file = open('leddata.txt','w')
		signal = 'left'
		file.write(signal)
		file.close()
		
	def callback_dis(self, data):
		#if self.waitDist == False:
		#if self.order == 3:
		self.waitDist = True
		#print("distance: ", self.order)
		msg = data.data
		msg = msg.split(' ')
		msg = list(map(int, msg))
		self.dis = msg
		#if self.order == 3:
		print("---distance---")

		print(self.dis)
		self.waitDist = False
		self.order = 4
#         if msg[0] <= 15:
#             self.steer = 
		

	def callback_main(self, data):

		#------------COMMAND INIT-----------

		if self.once == 1:
			command = {'action': '4', 'activate': True}
			self.sendCommand(command)
			#time.sleep(0.01)
			#self.parallel_parking()

			
			self.once = 0
			self.order = 4
		#-----------------------MAIN----------------------
		#if self.waitMain == False:
		if self.order == 4:
			
			if self.dis[0] > 0 and self.dis[0] < 20:
			    self.speed = 0.0
			    if self.pause == True:
			        command = {'action': '1', 'speed': self.speed}
			        self.sendCommand(command)
			if self.dis[7] > 0 and self.dis[7] < 20:
			    self.speed = 0.0
			    if self.pause == True:
			        command = {'action': '1', 'speed': self.speed}
			        self.sendCommand(command)
			        
			if self.dis[1] < 10:
				self.steer = 23.0
				command = {'action': '2', 'steerAngle': self.steer}
				self.sendCommand(command)
				
			if self.dis[6] < 10:
				self.steer = -23.0
				command = {'action': '2', 'steerAngle': self.steer}
				self.sendCommand(command)
				
			#front_side = self.dis[5]-self.dis[2]
			#if (self.dis[2] > 0 and self.dis[2] < 10) and (self.dis[5] > 0 and self.dis[5] < 10):
			#    self.steer = front_side*23/10
			#    if self.pause == True:
			#        command = {'action': '2', 'steerAngle': self.steer}
			#        self.sendCommand(command)
			#elif (self.dis[2] > 0 and self.dis[2] < 10): 
			#    self.steer = 23.0
			#    if self.pause == True:
			#        command = {'action': '2', 'steerAngle': self.steer}
			#        self.sendCommand(command)
			#elif (self.dis[5] > 0 and self.dis[5] < 10): 
			#    self.steer = -23.0
			#    if self.pause == True:
			#        command = {'action': '2', 'steerAngle': self.steer}
			#        self.sendCommand(command)
			
			
			#self.waitMain = True


			# if self.signState == 'stop':
			    # self.fstop()
			
			
			
			
			if self.pause == False:
			    print("---main---")
			    
			    if self.passRight == True and self.dis[6] == 0:
			        self.switchlane(0.2, "right")

			    command = {'action': '1', 'speed': self.speed}
			    self.sendCommand(command)
			    #time.sleep(0.001)

			    command = {'action': '2', 'steerAngle': self.steer}
			    self.sendCommand(command)
			    #time.sleep(0.001)
			    self.order = 2
			    #print(self.order)
			    self.waitMain = False
			   
			#command = {'action': '4', 'activate': True}
			#self.sendCommand(command)
			
if __name__ == '__main__':
	try:
		nod = AutomatedControlTransmitterProcess()

	except rospy.ROSInterruptException:
		pass
