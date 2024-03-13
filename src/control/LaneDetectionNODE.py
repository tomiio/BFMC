#!/usr/bin/env python3
from sklearn.cluster import DBSCAN
import rospy
import json
import cv2
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String
from std_msgs.msg import Bool
from cv_bridge import CvBridge, CvBridgeError
from laneprocessing.LaneProcessing import ClusterLane
from scipy.signal import butter, lfilter, freqz


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

class CameraHandler_test():
    # ===================================== INIT==========================================
    def __init__(self):
        """
        Creates a bridge for converting the image from Gazebo image intro OpenCv image
        """
        self.bridge = CvBridge()
        self.cv_image = np.zeros((640, 480))
        self.src_img = self.cv_image
        
        # image 
        self.show_image = True 
        self.record = True
        # Filter middle point
        self.SIZE_OF_FILTER = 10
        
        # Coeff array
        self.coeff = [1 for i in range(self.SIZE_OF_FILTER) ]
        self.coeff[-1] = 1
        self.list_middle_point = []
        self.lane_processor = ClusterLane(
                                one_lane_bias = 150, 
                                center_image = 320, 
                                num_points_to_center = 11, 
                                y_middle_point = 10,
                                top_crop = 280,
                                bot_crop = 480,
                                draw_line = True
                                )
        
        if self.record:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter('video_8_3_2024_full_map.avi', fourcc, 30.0, (640,480))
        
        rospy.init_node('LaneDetectionNODE', anonymous=True)
        self.image_sub = rospy.Subscriber("/automobile/image_raw", Image, self.callback, queue_size = 1, buff_size = 2**24)
        self.publisher = rospy.Publisher('/middlePoint_data', String, queue_size = 1)
        # 'x': middle_point , 'intersection' : intersection, 'pass': True
        
        rospy.spin()
         

    def callback(self, data):
        """
        :param data: sensor_msg array containing the image in the Gazsbo format
        :return: nothing but sets [cv_image] to the usefull image that can be use in opencv (numpy array)
        """
        self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        
        self.src_img = self.cv_image
        src_img = self.cv_image.copy()
        src_img = cv2.resize(src_img,(640,480))
        
        if self.record:
            self.out.write(src_img)
        
        try:
            # Process Lane
            self.lane_processor.cluster_lane(src_img)

            # Get data processed
            image_out = self.lane_processor.img
            middle_point = self.lane_processor.middle_point[0]
            intersection = self.lane_processor.get_intersection()
            self.list_middle_point.append(middle_point)
            # print(self.list_middle_point)
            
            if len(self.list_middle_point) == (self.SIZE_OF_FILTER):
                
                middle_point_array = np.array(self.list_middle_point.copy())
                coff_array = np.array(self.coeff.copy())
                _out_multi = middle_point_array*coff_array
                _out_multi = np.mean(_out_multi)
                
                middle_point = int(_out_multi.item())
                
                # middle_point = int(butter_lowpass_filter(self.list_middle_point, 3, 20, order=15)[-1])
                self.list_middle_point.pop(0)
            
            pub = {'x': middle_point , 'intersection' : intersection, 'pass': True}
            
            pub = json.dumps(pub)
            # print(pub)
            
            if self.show_image:
                # Draw middle point
                cv2.circle(image_out,(middle_point, 10 ), 5, (188, 144, 255), thickness=7, lineType=cv2.LINE_AA)
                cv2.imshow("image out", image_out)
                cv2.waitKey(1)
            
            self.publisher.publish(pub)

        except:
            print("errror")
            

if __name__ == '__main__':
    try:
        nod = CameraHandler_test()
    except rospy.ROSInterruptException:
        pass