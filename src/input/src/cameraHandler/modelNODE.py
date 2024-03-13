#!/usr/bin/env python3

# Copyright (c) 2019, Bosch Engineering Center Cluj and BFMC organizers
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
        
import io
import numpy as np
import time
import cv2

import rospy

from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String

from utils.utils import BaseEngine
import numpy as np
import cv2
import time
from sign_processing.SignDetectionTask import SignProcess
latest_msg = None

class Predictor(BaseEngine):
    def __init__(self, engine_path):
        super(Predictor, self).__init__(engine_path)
        self.n_classes = 13  # your model classes
        self.class_names = ['car', 'crosswalk', 'highway_entry', 'highway_exit', 'no_entry', 'onewayroad', 'parking', 'pedestrian', 'priority', 'roundabout', 'stop', 'trafficlight']

class modelNODE():
    def __init__(self):
        """The purpose of this nodeis to get the images from the camera with the configured parameters
        and post the image on a ROS topic. 
        It is able also to record videos and save them locally. You can do so by setting the self.RecordMode = True.
        """

        rospy.init_node('modelNODE', anonymous=False)

        # Image publisher object
        # self.image_publisher = rospy.Publisher("/automobile/image_raw", Image, queue_size=1)
        rospy.Subscriber("/automobile/image_raw", Image, self.get_msg)
        self.publisher = rospy.Publisher('/automobile/signs_task', String, queue_size = 1)
        
        engine = "/home/proe/Documents/Brain_ROS/src/input/src/cameraHandler/bfmc_7_3_2024.trt"
        self.pred = Predictor(engine_path=engine)
        self.pred.get_fps()
        self.bridge = CvBridge()

    def get_msg(self,msg):
        global latest_msg
        latest_msg = msg

    #================================ RUN ================================================
    def _streams(self):
        """Apply the initializing methods and start the thread. 
        """
        
        sign_process = SignProcess(self.publisher)
        
        rate = rospy.Rate(1000)
        while not rospy.is_shutdown():
            if latest_msg is not None:
                try:
                    frame = self.bridge.imgmsg_to_cv2(latest_msg, "bgr8")
                    image_ = frame.copy()
                
                    final_boxes, final_scores, final_cls_inds = self.pred.detect(frame, conf=0.6)
                    
                    sign_process.update(final_boxes, final_scores, final_cls_inds, image_)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                except CvBridgeError as e:
                    print(e)
            rate.sleep()
            

if __name__ == "__main__":
    camNod = modelNODE()
    camNod._streams()