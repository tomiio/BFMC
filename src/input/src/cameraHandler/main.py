from utils.utils import BaseEngine
import numpy as np
import cv2
import time

class Predictor(BaseEngine):
    def __init__(self, engine_path):
        super(Predictor, self).__init__(engine_path)
        self.n_classes = 13  # your model classes
        self.class_names = ['car', 'crosswalk', 'highway_entry', 'highway_exit', 'no_entry', 'onewayroad', 'parking', 'pedestrian', 'priority', 'roadblock', 'roundabout', 'stop', 'trafficlight']
if __name__ == '__main__':

    engine = "bfmc_yolov8.trt"
    pred = Predictor(engine_path=engine)
    pred.get_fps()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame,(640,480))
        #cv2.imshow("frame", frame)
        pred.detect(frame)
        if cv2.waitKey(50) & 0xFF == ord('q'):
        	break
    cap.release()
    cv2.destroyAllWindows()
