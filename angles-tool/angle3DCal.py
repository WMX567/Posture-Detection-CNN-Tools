"""
Calculate 3D angle
Angles estimated from CNN
Angles tracked by sensor
return elbow, shoulder, back, knee, neck angles
wumengxi@umich.edu
"""
import numpy as np
import matplotlib.pyplot as plt
from maker17 import calculate_vector_sensor_left_17, calculate_vector_sensor_right_17
from left import calculate_vector_cnn_left, calculate_vector_sensor_left
from right import calculate_vector_cnn_right, calculate_vector_sensor_right

index_cnn_right = [[3, 2, 12, 13], [8, 9], [11, 12], [10, 11], [1, 2], [0, 1]]
index_sensor_right = [[0, 3, 9, 12], [7, 8], [9, 10], [10, 11], [12, 13], [13, 14]]
index_cnn_left = [[2, 3, 12, 13], [8, 9], [14, 13], [15, 14], [4, 3], [5, 4]]
index_sensor_left = [[0, 3, 9, 12], [8, 7], [4, 3], [5, 4], [1, 0], [2, 1]]
index_sensor_left_17 = [[0, 3, 10, 14], [8, 9], [4, 3], [5, 4], [1, 0], [2, 1]]
index_sensor_right_17 = [[0, 3, 10, 14], [8, 9], [10, 11], [11, 12], [14, 15], [15, 16]]

def calculate_angle(v1, v2):
    cross_product = np.cross(v1, v2)
    dot_product = np.dot(v1, v2)
    angle = np.arctan2(np.linalg.norm(cross_product), dot_product)
    angle = angle/2/np.pi*360
    return angle

def calculation_validation(x, y, z, index_check_lists):
    bool_values = [1]*6
    for i in range(len(index_check_lists)):
        for j in index_check_lists[i]:
            if x[j] == -4111 or y[j] == -4111:
                bool_values[i] = 0
            elif j <= 14 and z[j] == -4111:
                bool_values[i] = 0
            if bool_values[i] == 0:
                break
    return bool_values

def proccess_3D_angles(x, y, z, is_truth):
    angles_3D, index_check_lists = ([] for i in range(2))
    if is_truth == True:
        bool_values = calculation_validation(x, y, z, index_sensor_left)
        vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee = calculate_vector_sensor_left(x, y, z, bool_values)
    else:
        bool_values = calculation_validation(x, y, z, index_cnn_left)
        vec_back, vec_head, vec_arm, vec_elbow, vec_leg, vec_knee = calculate_vector_cnn_left(x, y, z, bool_values)
    vertical_up = [0, -1, 0]
    elbow, knee, neg_vec_back, shoulder, back, neck = ([] for i in range(6))
    if vec_arm and vec_elbow:
        elbow = calculate_angle(vec_arm, vec_elbow)
    if vec_back:
        if is_truth == True:
            vertical_up = [-1, 0, 0]
        back = calculate_angle(vertical_up, vec_back)
    if vec_leg and vec_knee:
        knee = calculate_angle(vec_knee, vec_leg)
    if vec_back and vec_arm:
        neg_vec_back = [v * (-1) for v in vec_back]
        shoulder = calculate_angle(neg_vec_back, vec_arm)
    if vec_back and vec_head:
        neck = calculate_angle(vec_head, vec_back)
    angles_3D = [elbow, shoulder, back, knee, neck]
    vectors = [vec_arm, vec_elbow, vec_back, vec_leg, vec_knee, vec_head]
    if is_truth == True:
        angles_3D = [angle if angle else -4111 for angle in angles_3D]
    print(angles_3D)
    return angles_3D, vectors
