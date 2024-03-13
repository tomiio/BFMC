import numpy as np
import cv2

def get_bbd(points):
    """
    Get bounding box from a group of data points

    Parameters:
    - points

    Returns:
    - bounding_box

    """
    points = np.array(points)
    # Tìm giá trị x và y tối thiểu và tối đa
    x_min, y_min = np.min(points, axis=0)
    x_max, y_max = np.max(points, axis=0)

    # Hộp giới hạn được xác định bởi các điểm (x_min, y_min) và (x_max, y_max)
    bounding_box = np.array([[x_min, y_min], [x_max, y_max]])

    return bounding_box

def caculate_average_pixel_from_line(A, B, image, num_points = 10):
    """
    Caculate average pixel from N points between 2 points A,B

    Parameters:
    - A
    - B
    - num_points

    Returns:
    - average_pixel_value
    """
    # Tính vector từ A đến B
    vector_AB = np.array([B[0] - A[0], B[1] - A[1]])

    # Tạo 10 điểm trên đoạn thẳng AB
    points = [(A[0] + (vector_AB[0] * i / (num_points - 1)), A[1] + (vector_AB[1] * i / (num_points - 1))) for i in range(num_points)]

    mean = 0
    std = 0
    points_noisy = [] 
    for point in points:
        point += np.random.normal(mean, std, 2)
        
        x_ = point[0]
        y_ = point[1]
        
        if x_> image.shape[0]:
            x_ = image.shape[0]
        elif x_ < 0:
            x_ = 0

        if y_ > image.shape[1]:
            y_ = image.shape[1]
        elif y_ < 0 :
            y_ = 0
        
        points_noisy.append([x_, y_])
    # Đọc và tính trung bình giá trị pixel tại 10 điểm
    pixel_values = [image[int(point[1]), int(point[0])] for point in points_noisy]
    average_pixel_value = np.mean(pixel_values, axis=0)

    # print("10 điểm trên đoạn thẳng AB:", points)
    # print("Trung bình giá trị pixel tại 10 điểm:", average_pixel_value)

    return average_pixel_value

def sort_by_index(list_input = [[0,1,3],[3,4,5],[2,5,6]], dims = 1):
    """
    Sort by second element of list

    Parameters:
    - list

    Returns:
    - sorted list
    """
    return  sorted(list_input, key=lambda x: x[dims])

def find_index_2_lane(points = [(318, 200), (310, 250), (319, 300)] , target_x = 320):
    """
    Find index of data between a center point

    Parameters:
    - points
    - target

    Returns:
    - left_index
    - right_index
    """
    # Tìm giá trị x gần nhất bên trái và bên phải
    left = None
    right = None
    min_diff_left = float('inf')
    min_diff_right = float('inf')

    for x, _ in points:
        if x < target_x and (target_x - x) < min_diff_left:
            min_diff_left = target_x - x
            left = x
        elif x > target_x and (x - target_x) < min_diff_right:
            min_diff_right = x - target_x
            right = x

    # Tìm vị trí của các giá trị trong danh sách
    left_index = None
    right_index = None

    if left is not None:
        left_index = [i for i, (x, _) in enumerate(points) if x == left][0]

    if right is not None:
        right_index = [i for i, (x, _) in enumerate(points) if x == right][0]

    return left_index, right_index

def conert_to_binary(image):
    """
    Convert image to Black&White image

    Parameters:
    - image

    Returns:
    - Binary image
    """
    # # Chuyển đổi ảnh sang không gian màu LAB
    # lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # # Tách các kênh L, A, và B
    # l, a, b = cv2.split(lab)

    # # Cân bằng kênh L (độ sáng)
    # l_equalized = cv2.equalizeHist(l)

    # # Gộp các kênh lại với nhau
    # lab_equalized = cv2.merge((l_equalized, a, b))

    # # Chuyển đổi lại sang không gian màu BGR
    # image_equalized = cv2.cvtColor(lab_equalized, cv2.COLOR_LAB2BGR)
    
    # Chuyển đổi ảnh sang trắng đen (ảnh xám)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Áp dụng ngưỡng hóa để chuyển đổi sang ảnh nhị phân
    # 127 là giá trị ngưỡng, 255 là giá trị được gán cho các pixel vượt qua ngưỡng
    # cv2.THRESH_BINARY là kiểu ngưỡng hóa
    ret, binary_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

    return binary_image