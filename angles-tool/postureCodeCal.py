"""
postureCodeCal.py
Read the estimated join positions from CNN
Caculate the body angles based on the estimated join positions
Output a csv file contains the posture codes that correspond to the body angles
wumengxi@umich.edu
"""
import os,csv
import numpy as np
from ReadModelOutput import read_model_output, modify_filename

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path，'FinalSkeleton')
output_path = os.path.join(dir_path，'PostureCodes')
angles = []

def calculate_angle(v1, v2):
    cross_product = np.cross(v1, v2)
    dot_product = np.dot(v1, v2)
    angle = np.arctan2(np.linalg.norm(cross_product), dot_product)
    return angle/2/np.pi*360

def upper_limb_estimate(shoulder_angle, elbow_angle):
    upper_limb_code = 10
    if shoulder_angle < 15:
        if elbow_angle < 45:
            upper_limb_code = 0
        else:
            upper_limb_code = 1
    elif shoulder_angle >= 15 and shoulder_angle < 45:
        if elbow_angle < 45:
            upper_limb_code = 3
        else:
            upper_limb_code = 2
    elif shoulder_angle >= 45 and shoulder_angle < 75:
        if elbow_angle < 45:
            upper_limb_code = 5
        else:
            upper_limb_code = 4
    elif shoulder_angle >= 75 and shoulder_angle < 100:
        if elbow_angle < 45:
            upper_limb_code = 7
        else:
            upper_limb_code = 6
    elif shoulder_angle >= 100 and shoulder_angle < 140:
        upper_limb_code = 8
    elif shoulder_angle >= 140 and shoulder_angle < 180:
        upper_limb_code = 9
    return upper_limb_code

def back_estimate(back_angle):
    back_code = 0
    if back_angle < 10:
        back_code = 1
    elif back_angle >= 10 and back_angle < 30:
        back_code = 4
    elif back_angle >= 30 and back_angle < 65:
        back_code = 7
    elif back_angle >= 65 and back_angle < 180:
        back_code = 9
    return back_code

def knee_estimate(knee_angle):
    knee_code = -1
    if knee_angle < 45:
        knee_code = 0
    else:
        knee_code = 8
    return knee_code

def neck_estimate(neck_angle):
    neck_code = -1
    if neck_angle < 20:
        neck_code = 0
    elif neck_angle >= 20:
        neck_code = 1
    return neck_code

def proccess_one_image_2D_angle(x, y):
    posture_codes = []
    #计算向量
    #vec_back = [(x[12]+x[13]-x[3]-x[2])/2, (y[12]+y[13]-y[3]-y[2])/2, 0]
    vec_back = [x[12]-x[3], y[12]-y[3], 0]
    vec_head = [x[9]-x[8], y[9]-y[8], 0]
    vec_left_arm = [x[14]-x[13], y[14]-y[13], 0]
    vec_left_elbow = [x[15]-x[14], y[15]-y[14], 0]
    vec_left_leg = [x[4]-x[3], y[4]-y[3], 0]
    vec_left_knee = [x[5]-x[4], y[5]-y[4], 0]
    vertical_up = [0, -1, 0]
    #计算角度
    elbow_angle = calculate_angle(vec_left_arm, vec_left_elbow)
    knee_angle = calculate_angle(vec_left_leg, vec_left_knee)
    neg_vec_back = [v * (-1) for v in vec_back]
    shoulder_angle = calculate_angle(neg_vec_back, vec_left_arm)
    back_angle = calculate_angle(vertical_up, vec_back)
    neck_angle = calculate_angle(vec_back, vec_head)
    #预测posture codes
    angles.append([elbow_angle, shoulder_angle, back_angle, knee_angle, neck_angle])
    posture_codes.append(upper_limb_estimate(shoulder_angle, elbow_angle))
    posture_codes.append(back_estimate(back_angle))
    posture_codes.append(knee_estimate(knee_angle))
    posture_codes.append(neck_estimate(neck_angle))
    return posture_codes

if __name__ == "__main__":
    files = os.listdir(input_path)
    for filename in files:
        print(filename)
        if filename == '.DS_Store' or filename == '.DS_Store.csv':
            continue
        vision_result, vision_sampled = ([] for i in range(2))
        input_file = input_path + filename
        X, Y, video_frames = read_model_output(input_file)
        for x_values, y_values in zip(X, Y):
            posture_codes = proccess_one_image_2D_angle(x_values, y_values)
            vision_result.append(posture_codes)
        read_length = int(len(vision_result)/6)
        for i in range(read_length):
            print('Frame:', i*6)
            print('Sample:', vision_result[i*6])
            vision_sampled.append(vision_result[i*6])
        modified = modify_filename(filename)
        print('filename:', modified)
        with open(output_path + modified + '.csv', 'w') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(vision_result)


