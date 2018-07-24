"""
Calculate 3D angle
Angles estimated from CNN
Angles tracked by sensor
return elbow, shoulder, back, knee, neck angles
wumengxi@umich.edu
"""
import numpy as np
import matplotlib.pyplot as plt

def calculate_angle(v1, v2):
    cross_product = np.cross(v1, v2)
    dot_product = np.dot(v1, v2)
    angle = np.arctan2(np.linalg.norm(cross_product), dot_product)
    angle = angle/2/np.pi*360
    return angle

def calculate_vector_cnn(x, y, z, bool_values):
    vec_back, vec_head, vec_left_arm, vec_left_elbow, vec_left_leg, vec_left_knee = ([] for i in range(6))
    if bool_values[0]:
        """print('x[12]:', x[12], 'x[13]:', x[13], 'x[3]:', x[3], 'x[2]:', x[2])
        print('y[12]:', y[12], 'y[13]:', y[13], 'y[3]:', x[3], 'y[2]:', x[2])
        print('z[12]:', z[12], 'z[13]:', z[13], 'z[3]:', z[3], 'z[2]:', z[2])"""
        vec_back = [(x[12]+x[13]-x[3]-x[2])/2, (y[12]+y[13]-y[3]-y[2])/2, (z[12]+z[13]-z[3]-z[2])/2]
        #print('vec_back:', vec_back)
    if bool_values[1]:
        """print('x[9]:', x[9], 'x[8]:', x[8], 'y[9]:', y[9], 'y[8]:', y[8], 'z[8]:', z[8], 'z[9]:', z[9])"""
        vec_head = [x[9]-x[8], y[9]-y[8], z[9]-z[8]]
        #print('vec_head:', vec_head)
    if bool_values[2]:
        """print('x[14]:', x[14], 'x[13]:', x[13], 'y[14]:', y[14], 'y[13]:', y[13], 'z[14]:', z[14], 'z[13]:', z[13])"""
        vec_left_arm = [x[14]-x[13], y[14]-y[13], z[14]-z[13]]
        #print('vec_left_arm:', vec_left_arm)
    if bool_values[3]:
        """print('x[15]:', x[15], 'x[14]:', x[14], 'y[15]:', y[15])"""
        vec_left_elbow = [x[15]-x[14], y[15]-y[14], 0]
        #print('vec_left_elbow:', vec_left_elbow)
    if bool_values[4]:
        """print('x[4]:', x[4], 'x[3]:', x[3], 'y[4]:', y[4], 'y[3]:', y[3], 'z[4]:', z[4], 'z[3]:', z[3])"""
        vec_left_leg = [x[4]-x[3], y[4]-y[3], z[4]-z[3]]
        #print('vec_left_leg:', vec_left_leg)
    if bool_values[5]:
        """print('x[5]:', x[5], 'x[4]:', x[4], 'y[5]:', y[5], 'y[4]:', y[4], 'z[5]:', z[5], 'z[4]:', z[4])"""
        vec_left_knee = [x[5]-x[4], y[5]-y[4], z[5]-z[4]]
        #print('vec_left_knee:', vec_left_knee)
    return vec_back, vec_head, vec_left_arm, vec_left_elbow, vec_left_leg, vec_left_knee

def calculate_vector_sensor(x, y, z, bool_values):
    vec_back, vec_head, vec_left_arm, vec_left_elbow, vec_left_leg, vec_left_knee = ([] for i in range(6))
    if bool_values[0]:
        """print('x[3]:', x[3], 'x[9]:', x[9], 'x[0]:', x[0], 'x[12]:', x[12])
        print('y[3]:', y[3], 'y[9]:', y[9], 'y[0]:', x[0], 'y[12]:', x[12])
        print('z[3]:', z[3], 'z[9]:', z[9], 'z[0]:', z[0], 'z[12]:', z[12])"""
        vec_back = [(x[3]+x[9]-x[0]-x[12])/2, (y[3]+y[9]-y[0]-y[12])/2, (z[3]+z[9]-z[0]-z[12])/2]
        #print('vec_back:', vec_back)
    if bool_values[1]:
        #print('x[8]:', x[8], 'x[7]:', x[7], 'y[8]:', y[8], 'y[7]:', y[7], 'z[8]:', z[8], 'z[7]:', z[7])
        vec_head = [x[8]-x[7], y[8]-y[7], z[8]-z[7]]
        #print('vec_head:', vec_head)
    if bool_values[2]:
        #print('x[4]:', x[4], 'x[3]:', x[3], 'y[4]:', y[4], 'y[3]:', y[3], 'z[4]:', z[4], 'z[3]:', z[3])
        vec_left_arm = [x[4]-x[3], y[4]-y[3], z[4]-z[3]]
        #print('vec_left_arm:', vec_left_arm)
    if bool_values[3]:
        #print('x[5]:', x[5], 'x[4]:', x[4], 'y[5]:', y[4], 'z[5]', z[5], 'z[4]:', z[4])
        vec_left_elbow = [x[5]-x[4], y[5]-y[4], z[5]-z[4]]
        #print('vec_left_elbow:', vec_left_elbow)
    if bool_values[4]:
        #print('x[1]:', x[1], 'x[0]:', x[0], 'y[1]:', y[0], 'z[1]', z[1], 'z[0]:', z[0])
        vec_left_leg = [x[1]-x[0], y[1]-y[0], z[1]-z[0]]
        #print('vec_left_leg:', vec_left_leg)
    if bool_values[5]:
        #print('x[2]:', x[2], 'x[1]:', x[1], 'y[2]:', y[2], 'y[1]', y[1], 'z[1]', z[2], 'z[1]:', z[1])
        vec_left_knee = [x[2]-x[1], y[2]-y[1], z[2]-z[1]]
        #print('vec_left_knee:', vec_left_knee)
    return vec_back, vec_head, vec_left_arm, vec_left_elbow, vec_left_leg, vec_left_knee

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
        index_check_lists = [[0, 3, 9, 12], [8, 7], [4, 3], [5, 4], [1, 0], [2, 1]]
        bool_values = calculation_validation(x, y, z, index_check_lists)
        vec_back, vec_head, vec_left_arm, vec_left_elbow, vec_left_leg, vec_left_knee = calculate_vector_sensor(x, y, z, bool_values)
    else:
        index_check_lists = [[2, 3, 12, 13], [8, 9], [14, 13], [15, 14], [4, 3], [5, 4]]
        bool_values = calculation_validation(x, y, z, index_check_lists)
        vec_back, vec_head, vec_left_arm, vec_left_elbow, vec_left_leg, vec_left_knee = calculate_vector_cnn(x, y, z, bool_values)
    vertical_up = [0, -1, 0]
    elbow, knee, neg_vec_back, shoulder, back, neck = ([] for i in range(6))
    if vec_left_arm and vec_left_elbow:
        elbow = calculate_angle(vec_left_arm, vec_left_elbow)
    if vec_back:
        if is_truth == True:
            vertical_up = [-1, 0, 0]
        back = calculate_angle(vertical_up, vec_back)
    if vec_left_leg and vec_left_knee:
        knee = calculate_angle(vec_left_knee, vec_left_leg)
    if vec_back and vec_left_arm:
        neg_vec_back = [v * (-1) for v in vec_back]
        shoulder = calculate_angle(neg_vec_back, vec_left_arm)
    if vec_back and vec_head:
        neck = calculate_angle(vec_head, vec_back)
    angles_3D = [elbow, shoulder, back, knee, neck]
    vectors = [vec_left_arm, vec_left_elbow, vec_back, vec_left_leg, vec_left_knee, vec_head]
    if is_truth == True:
        angles_3D = [angle if angle else -4111 for angle in angles_3D]
    print(angles_3D)
    return angles_3D, vectors
    




