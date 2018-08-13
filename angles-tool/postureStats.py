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
from ReadModelOutput import modify_filename

dir_path = os.path.dirname(os.path.realpath(__file__))
vision_path = os.path.join(dir_path, 'PostureCodes')
truth_path = os.path.join(dir_path, 'Ground_Truth')
output_path = os.path.join(dir_path, 'Confusion_Matrix')
param_path = os.path.join(dir_path, 'truth_correspond.csv')

def mapping(vision_filename):
    video_ID = ''
    subject_ID = int(vision_filename[0:2])
    video_cut = vision_filename[-1]
    print('video:', video_cut)
    if len(vision_filename) > 10:
        video_cut = vision_filename[-3:]
    with open(param_path, encoding='utf-8', errors='replace') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Subject ID'] != '':
                if int(row['Subject ID']) == subject_ID:
                    video_ID = row['Video ID']
                    break
    pad_zero = '0'
    if len(video_ID) < 3:
        pad_zero = '00'
    truth_filename = vision_filename[0:2] + '_' + pad_zero + video_ID + '_' + 'S' + video_cut
    return truth_filename

def count_postureCode(vision_filename):
    truth_filename = mapping(vision_filename)
    read_truth = pd.read_csv(os.path.join(truth_path, truth_filename + '.csv'), encoding = 'utf8').dropna(how='all')
    read_vision = pd.read_csv(os.path.join(vision_path, vision_filename + '.csv'), encoding = 'utf8').dropna(how='all')
    truth = read_truth.values.tolist()
    vision = read_vision.values.tolist()
    return truth, vision

if __name__ == "__main__":
    vision_files = os.listdir(vision_path)
    for filename in vision_files:
        if filename != '.DS_Store' and filename != '.DS_Store.csv':
            #打散Video的名称
            #每一个新的Video都有一个新的Directory
            #根据S2或者S4分类
            upper_limbs_truth, upper_limbs_vision, back_truth, back_vision = ([] for i in range(4))
            leg_truth, leg_vision, neck_truth, neck_vision = ([] for i in range(4))
            print('File used: ', filename)
            vision_filename = modify_filename(filename)
            vision_filename = vision_filename.replace('.csv', '')
            #打散Video的名称
            video_ID = vision_filename[3:7]
            print('Video ID:', video_ID)
            video_path = os.path.join(output_path, video_ID)
            if not os.path.exists(video_path):
                os.makedirs(video_path)
            truth, vision = count_postureCode(vision_filename)
            upper_limbs_truth.extend(list(map(int, truth[0])))
            back_truth.extend(list(map(int, truth[1])))
            leg_truth.extend(list(map(int, truth[2])))
            neck_truth.extend(list(map(int, truth[3])))
            upper_limbs_vision.extend(vision[0])
            back_vision.extend(vision[1])
            leg_vision.extend(vision[2])
            neck_vision.extend(vision[3])
            truth = [upper_limbs_truth, back_truth, leg_truth, neck_truth]
            vision = [upper_limbs_vision, back_vision, leg_vision, neck_vision]
            #新建一个Directory
            new_path = os.path.join(video_path, vision_filename + '_CM')
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            options = ['Upper Limb','Back','Knee','Neck']
            for i in range(len(truth)):
                print_stdout = sys.stdout
                out_file = open(os.path.join(new_path, options[i] + '_CM.txt'), 'w')
                sys.stdout = out_file
                con_matrix = ConfusionMatrix(truth[i], vision[i])
                print(con_matrix)
                sys.stdout = print_stdout
                out_file.close()
