import numpy as np
import cv2
import os

def detect_traffic_light_color(image, x0, y0, x1, y1):
    # Đọc ảnh và chuyển sang ảnh xám

    image_crop = image[y0 :y1 , x0: x1]
    
    gray_image = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)

    # Sử dụng GaussianBlur để giảm nhiễu
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    h = y1 - y0
    # Lấy phần ảnh tương ứng với bounding box
    
    cv2.imshow("roi", blurred_image)
    # Tính ngưỡng sáng (có thể điều chỉnh tùy thuộc vào điều kiện ánh sáng)
    brightness_threshold = 200
    _, thresh = cv2.threshold(blurred_image, brightness_threshold, 255, cv2.THRESH_BINARY)
    total_thresh = np.sum(thresh) // 255
    if total_thresh < 20:
        return 0
        # return "off"
    upper_half = np.sum(thresh[:int(h//2)-20, :]) // 255
    lower_half = np.sum(thresh[int(h//2)-20:, :])
    if upper_half > 120 or lower_half > 120:
        if upper_half > lower_half:
            return 0
            # return "green" 
        else:
            return 1
            # return "red"
    else:
        return 1
        # return "yellow"
        
