import json
from sign_processing.TrafficLightClassification import detect_traffic_light_color
class SignProcess():
    def __init__(self, publisher, 
                num_signs = 10, 
                nums_task = 12,
                conf_thresh = 0.5,
                conf_add = 0.8,
                conf_reset = 0,
                h_size = 80,

                ) -> None:
        
        self.publisher = publisher

        # init sign task process
        self.nums_signs = num_signs
        self.conf_thresh = conf_thresh
        self.conf_add = conf_add
        self.conf_reset = conf_reset
        self.nums_task = nums_task
        self.h_size = h_size

        # init list tasks
        self.list_all_task = []
        self.list_check_pub = []
        
        for i in range(self.nums_task):
            self.list_all_task.append([0 for i in range(self.nums_signs)])
            self.list_check_pub.append(0)

    def update(self, final_boxes, final_score, final_cls_inds, image):
        # print(self.list_all_task)
        for cls_index in range(self.nums_task):
            self.list_all_task[cls_index].pop(0)
            self.list_all_task[cls_index].append(0)
    
        for i, box in enumerate(final_boxes):

            # get bounding box of object
            x_0 = int(box[0])
            y_0 = int(box[1])
            x_1 = int(box[2])
            y_1 = int(box[3])

            h_box = y_1 - y_0
            # get conf score
            conf_score = float(final_score[i])

            # get class index
            cls_index = int(final_cls_inds[i])

            if conf_score > self.conf_thresh:
                if h_box > self.h_size:
                    if cls_index == 11:
                        _check = detect_traffic_light_color(image, x_0, y_0, x_1, y_1 )  
                        print(_check)
                        self.list_all_task[cls_index][-1] = _check
                    else:
                        self.list_all_task[cls_index][-1] = 1


        for cls_index in range(self.nums_task):
            list_task = self.list_all_task[cls_index]
            len_list_task = len(list_task)

            if len_list_task == self.nums_signs :
                _conf = list_task.count(1)/self.nums_signs

                if _conf > self.conf_add and not self.list_check_pub[cls_index]:

                    self.list_check_pub[cls_index] = 1
                    msg = {"list_task": self.list_check_pub}
                    print(msg)
                    msg = json.dumps(msg)
                    self.publisher.publish(msg)
                    self.list_all_task[cls_index] = [0 for i in range(self.nums_signs)]
                    

                elif _conf == self.conf_reset:
                    self.list_check_pub[cls_index] = 0
                    
        # msg = {"list_task": self.list_check_pub}
        # print(msg)
        # msg = json.dumps(msg)
        # self.publisher.publish(msg)



    def reset():
        pass