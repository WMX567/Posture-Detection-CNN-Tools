"""
   postureStats.py
   Evaluate estimation results from CNN
   Output confusion matrix and accuracy score
   wumengxi@umich.edu
"""
import os,sys,csv
import pandas as pd
import numpy as np
from pycm import ConfusionMatrix

truth_path = '/Users/wumengxi/Desktop/Ground_T/'
vision_path = '/Users/wumengxi/Desktop/Vision_Tests/'
output_path = '/Users/wumengxi/Desktop/Confusion_Matrix/'

def count_postureCode(filename):
    read_truth = pd.read_csv(truth_path + filename, encoding = 'utf8').dropna(how='all')
    read_vision = pd.read_csv(vision_path + filename, encoding = 'utf8').dropna(how='all')
    truth = read_truth.values.tolist()
    vision = read_vision.values.tolist()
    return truth, vision

if __name__ == "__main__":
    truth_files = os.listdir(truth_path)
    upper_limbs_truth, upper_limbs_vision, back_truth, back_vision = ([] for i in range(4))
    leg_truth, leg_vision, neck_truth, neck_vision = ([] for i in range(4))
    for filename in truth_files:
        truth, vision = count_postureCode(filename)
        vision_sampled, video_frames = ([] for i in range(2))
        for i in range(len(truth)):
            video_frames.append([i*6])
            vision_sampled.append(vision[i*6])
        truth = list(map(list, zip(*truth)))
        vision = list(map(list, zip(*vision_sampled)))
        if filename != '.DS_Store':
            print('File used: ', filename)
            upper_limbs_truth.extend(list(map(int, truth[0])))
            back_truth.extend(list(map(int, truth[1])))
            leg_truth.extend(list(map(int, truth[2])))
            neck_truth.extend(list(map(int, truth[3])))
            upper_limbs_vision.extend(vision[0])
            back_vision.extend(vision[1])
            leg_vision.extend(vision[2])
            neck_vision.extend(vision[3])
    options = ['Upper Limb','Back','Knee','Neck']
    truth = [upper_limbs_truth, back_truth, leg_truth, neck_truth]
    vision = [upper_limbs_vision, back_vision, leg_vision, neck_vision]
    for i in range(len(truth)):
        print_stdout = sys.stdout
        out_file = open(output_path + options[i] + '_CM.txt', 'w')
        sys.stdout = out_file
        con_matrix = ConfusionMatrix(truth[i], vision[i])
        print(con_matrix)
        sys.stdout = print_stdout
        out_file.close()




