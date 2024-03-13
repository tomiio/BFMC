import cv2
import numpy as np
from sklearn.cluster import DBSCAN
from utils.utils import find_index_2_lane, sort_by_index, get_bbd, conert_to_binary, caculate_average_pixel_from_line

class ClusterLane:
    """
    Lane Process Class
    """
    def __init__(self, one_lane_bias = 120, 
                center_image = 320, 
                num_points_to_center = 10, 
                y_middle_point = 10,
                top_crop = 280,
                bot_crop = 480,
                draw_line = True
                ) -> None:
        """"
        Init parameter of lane process

        Parameters:
        - one_lane_bias = 120, 
        - center_image = 320, 
        - num_points_to_center = 5, 
        - y_middle_point = 10,
        - top_crop = 280,
        - bot_crop = 480,
        - draw_line = True

        Returns:
        -

        """
        self.one_lane_bias = one_lane_bias
        self.center_image = center_image
        self.num_points_to_center = num_points_to_center
        self.y_middle_point = y_middle_point
        self.top_crop = top_crop
        self.bot_crop = bot_crop
        self.draw_line = draw_line
        self.counts_intersection = 5
        self._count_intersection = False
        self.list_colers = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 0, 255),
            (0, 255, 255),
            (255, 0, 255),
            (0, 255, 255),
            (255, 0, 255),
            (0, 255, 255)
        ]
        
        self.angle_top = 15
        self.angle_bot = -15

        self.middle_point = [self.center_image, self.y_middle_point]
        self.img = None
        self.intersection = False
    
    def reset_counts(self):
        """
        Reset counter of intersection
        """
        self.counts_intersection = 5

    def cluster_lane(self, image):
        """ 
        Cluster lane from image

        Parameters:
        - image
        - top_crop
        - bot_crop

        Returns:
        - clusters of lane

        """

        top_crop = self.top_crop
        bot_crop = self.bot_crop

        # Crop IoU from origin image
        img_crop = image[top_crop:bot_crop,:]

        img = img_crop.copy()
        # Blur Image
        # blur = cv2.blur(img, (3,3))

        # Convert Image to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Get edges 
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Detect line from egdes
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 6, minLineLength=6, maxLineGap=0)
        
        list_points = []
        list_num_horizon = []
        # Create list points of line
        if lines is not None:
            
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if (y1 + y2)/2 < bot_crop - top_crop - 10:
                    
                    c_x = int((x1 + x2)/2)
                    c_y = int((y1 + y2)/2)
                    list_points.append([c_x, c_y])
                    list_points.append([x1, y1])
                    list_points.append([x2, y2])
        
        data = np.array(list_points)

        # Cluster lines 
        if len(data) > 0:

            clustering = DBSCAN(eps=80, min_samples=7).fit(data)
            labels = clustering.labels_
            
            list_clusters = []
            num_clusters = len(set(labels)) - (1 if -1 in labels else 0)

            for label_id in range(num_clusters):
                
                list_points = []
                for id, point in enumerate(data):

                    if labels[id] == label_id:
                        list_points.append(point)
                        if self.draw_line:
                            cv2.circle(img,(point[0], point[1] ),1, self.list_colers[label_id], thickness=3, lineType=cv2.LINE_AA)

                list_clusters.append(list_points)

            # Sort list of points after cluster
            sorted_list_bots = []
            sorted_list_tops = []
            for list_data in list_clusters:
                
                list_bot_sorted = sort_by_index(list_data)
                sorted_list_bots.append(list_bot_sorted)
                
                len_list_bot_sorted = int(len(list_bot_sorted)/2)
                sorted_list_tops.append(sort_by_index(list_bot_sorted[:len_list_bot_sorted], 0))

            list_bot_center = []
            list_top_center = []

            # Get last point
            for i, sorted_list_bot in enumerate(sorted_list_bots):

                sorted_list_top = sorted_list_tops[i]
                
                if len(sorted_list_top) > self.num_points_to_center:
                    
                    bot_center = np.mean(sorted_list_bot[-self.num_points_to_center:-1], axis=0, dtype=np.int32)
                    list_bot_center.append(bot_center)

                    # Check center is left or right of the image center
                    if bot_center[0] < self.center_image:
                        top_center = np.mean(sorted_list_top[-self.num_points_to_center:-1], axis=0, dtype=np.int32)
                    else:
                        top_center = np.mean(sorted_list_top[0: self.num_points_to_center], axis=0, dtype=np.int32)

                    list_top_center.append(top_center)
                    bdb_ = get_bbd(sorted_list_bot)
                    
                    x0 = bdb_[0][0]
                    y0 = bdb_[0][1]

                    x1 = bdb_[1][0]
                    y1 = bdb_[1][1]

                    # Conevert to Binary Image
                    # img_lane = img_crop[y0:y1, x0:x1].copy()
                    # binary_img = conert_to_binary(img_lane)
                    # cv2.imshow("lane", binary_img)

                    # draw points and bouding box
                    if self.draw_line:
                        cv2.rectangle(img, (x0, y0), (x1, y1), self.list_colers[-1], 2, cv2.LINE_AA)
                        cv2.circle(img,(bot_center[0], bot_center[1] ),1,(155,0,155), thickness=3, lineType=cv2.LINE_AA)
                        cv2.circle(img,(top_center[0], top_center[1] ),1,(155,0,155), thickness=3, lineType=cv2.LINE_AA)
       
            # Process 1 lane
            if len(list_bot_center) == 1:
                bot_data = list_bot_center[0]
                top_data = list_top_center[0]
                x_bot = bot_data[0]
                x_top = top_data[0]
                
                data_0 = np.array(sorted_list_bots[0])
                m_0, b_0 = np.polyfit(data_0[:,0], data_0[:,1], 1)
                angle_0 =  np.arctan(m_0)*180/np.pi

                if (self.angle_bot < angle_0 < self.angle_top):
                    if self.counts_intersection > 0:
                        self.counts_intersection -= 1
                    self._count_intersection = True
                    if self.counts_intersection == 0:
                        self.middle_point = [self.center_image, self.y_middle_point]
                        self.intersection = True
                        # self.reset_counts()

                elif x_bot > self.center_image:
                    self.middle_point = [int(x_top - self.one_lane_bias), self.y_middle_point]

                elif x_bot < self.center_image:
                    self.middle_point = [int(x_top + self.one_lane_bias), self.y_middle_point]
                
                else:
                    self.middle_point = self.middle_point

            # Process 2 lane
            elif len(list_bot_center) == 2:

                data_0 = np.array(sorted_list_bots[0])
                data_1 = np.array(sorted_list_bots[1])
                
                m_0, b_0 = np.polyfit(data_0[:,0], data_0[:,1], 1)
                angle_0 =  np.arctan(m_0)*180/np.pi
                
                m_1, b_1 = np.polyfit(data_1[:,0], data_1[:,1], 1)
                angle_1 = np.arctan(m_1)*180/np.pi

                # Get Points
                _bot_center_0 = list_bot_center[0]
                _bot_center_1 = list_bot_center[1]

                _top_center_0 = list_top_center[0]
                _top_center_1 = list_top_center[1]

                # Get X, Y
                _bot_x_0 = _bot_center_0[0]
                _bot_x_1 = _bot_center_1[0]

                _top_x_0 = _top_center_0[0]
                _top_x_1 = _top_center_1[0]

                if ( self.angle_bot < angle_0 < self.angle_top) or ( self.angle_bot < angle_1 < self.angle_top):
                    if self.counts_intersection > 0:
                        self.counts_intersection -= 1
                    self._count_intersection = True
                    if self.counts_intersection == 0:
                        self.middle_point = [self.center_image, self.y_middle_point]
                        self.intersection = True
                        # self.reset_counts()

                # elif (_bot_x_0 > self.center_image) and (_bot_x_1 > self.center_image):
                    
                #     cp_x = min(_top_x_0, _top_x_1)
                #     self.middle_point = [cp_x - self.one_lane_bias, self.y_middle_point]

                # elif _bot_x_0 < self.center_image and _bot_x_1 < self.center_image:
                    
                #     cp_x = max(_top_x_0, _top_x_1)
                #     self.middle_point = [cp_x + self.one_lane_bias, self.y_middle_point]

                # else:
                    
                #     cp_x = int((_top_x_0 + _top_x_1)/2)
                #     cp_y = self.y_middle_point
                #     self.middle_point = [cp_x, cp_y]
                
                # BOT MIDDLE POINT
                elif (_bot_x_0 > self.center_image) and (_bot_x_1 > self.center_image):
                    
                    cp_x = min(_bot_x_0, _bot_x_1)
                    self.middle_point = [cp_x - self.one_lane_bias, self.y_middle_point]

                elif _bot_x_0 < self.center_image and _bot_x_1 < self.center_image:
                    
                    cp_x = max(_bot_x_0, _bot_x_1)
                    self.middle_point = [cp_x + self.one_lane_bias, self.y_middle_point]

                else:
                    
                    cp_x = int((_bot_x_0 + _bot_x_1)/2)
                    cp_y = self.y_middle_point
                    self.middle_point = [cp_x, cp_y]

            # Process n lane
            elif len(list_bot_center) >= 3:
                left_index, right_index = find_index_2_lane(list_bot_center, 320)

                if left_index is None and right_index is None:
                    pass

                elif left_index is None:
                    if right_index > 0:
                        left_index = 0
                    else:
                        left_index = -1

                elif right_index is None:
                    if left_index > 0:
                        right_index = 0
                    else:
                        right_index = -1

                # left_point = list_top_center[left_index]
                # right_point = list_top_center[right_index]
                
                # BOT MIDDLE POINT
                left_point = list_bot_center[left_index]
                right_point = list_bot_center[right_index]

                x_left = left_point[0]
                x_right = right_point[0]

                x_center = int((x_left + x_right)/2)
                self.middle_point = [x_center, self.y_middle_point]
                
        self.img = img

    def get_intersection(self):
        """
        Check Intersection
        
        Parameters:
        -

        Returns:
        - is intersection or not
        """
        old_ = self.intersection
        self.intersection = False
        if not self._count_intersection :
            self.reset_counts()
        self._count_intersection = False
        return old_
    