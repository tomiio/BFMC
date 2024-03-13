#!/usr/bin/env python3
import serial
import json
import rospy
from std_msgs.msg      import String

class serialNODE():
    def __init__(self):
        """It forwards the control messages received from socket to the serial handling node. 
        """
        
        devFile = '/dev/ttyACM1'
        
        # comm init       
        self.serialCom = serial.Serial(devFile,115200,timeout=0.1)
        self.serialCom.flushInput()
        self.serialCom.flushOutput()
        
        rospy.init_node('serialReadNODE', anonymous=False)
        
        self.pub_imu = rospy.Publisher("/automobile/imu_data", String, queue_size=1)
        self.pub_distance = rospy.Publisher("/automobile/distance_data", String, queue_size=1)
        
     # ===================================== RUN ==========================================
    def run(self):
        """Apply the initializing methods and start the threads
        """
        rospy.loginfo("starting serialReadNODE")
        self._read()    
        
    # ===================================== READ ==========================================
    def _read(self):
        """ It's represent the reading activity on the the serial.
        """
        while not rospy.is_shutdown():
            read_chr=self.serialCom.readline()
            try:
                read_chr=(read_chr.decode("utf-8"))
                temp = read_chr.split(",")
                # print(temp)
                imu_msg = {'roll': temp[2], 
                           'pitch': temp[1], 
                           'yaw': temp[0], 
                           'accX': temp[3], 
                           'accY': temp[4], 
                           'accZ': temp[5]}
                # print(imu_msg)
    
                distance_msg = {'d1': temp[-5],
                                'd2': temp[-4],
                                'd3': temp[-3],
                                'd4': temp[-2],
                                'd5': temp[-1]}
                
                imu_msg = json.dumps(imu_msg)
                distance_msg = json.dumps(distance_msg)
                
                self.pub_imu.publish(imu_msg)
                
                self.pub_distance.publish(distance_msg)
            except UnicodeDecodeError:
                print("serialReadNODE error")
                pass
        
            
if __name__ == "__main__":
    serNod = serialNODE()
    serNod.run()
