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
import numpy as np
import cv2
import time


class cameraNODE():
	def __init__(self):
		"""The purpose of this nodeis to get the images from the camera with the configured parameters
		and post the image on a ROS topic. 
		It is able also to record videos and save them locally. You can do so by setting the self.RecordMode = True.
		"""
		self.cap = cv2.VideoCapture(0)
		self.cap.set(3,640)
		self.cap.set(4,480)
		#self.cap.set(5,30)


		rospy.init_node('cameraNODE', anonymous=False)

		# Image publisher object
		self.image_publisher = rospy.Publisher("/automobile/image_raw", Image, queue_size=1)

		self.bridge = CvBridge()

		# streaming options
		# self._stream      =   io.BytesIO()

		# self.recordMode   =   False

	#================================ RUN ================================================
	def run(self):
		"""Apply the initializing methods and start the thread. 
		"""

		while not rospy.is_shutdown():
			ret, frame = self.cap.read()
			try:
				imageObject = self.bridge.cv2_to_imgmsg(frame, "bgr8")
				imageObject.header.stamp = rospy.Time.now()
				self.image_publisher.publish(imageObject)
				
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			except CvBridgeError as e:
				print(e)
		
		self.cap.release()
		rospy.shutdown()
			

if __name__ == "__main__":
	camNod = cameraNODE()
	camNod.run()
