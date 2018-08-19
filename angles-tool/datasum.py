"""
   datasum.py
   Evaluate estimation results from CNN, Version 1.1
   Output confusion matrix and accuracy score
   wumengxi@umich.edu
"""
import os,sys,csv
import numpy as np
from ReadModelOutput import modify_filename
from confmatrix import confusion_matrix, print_confusion_matrix

dir_path = os.path.dirname(os.path.realpath(__file__))
vision_path = os.path.join(dir_path, 'PostureCodes')
truth_path = os.path.join(dir_path, 'Ground_Truth')
output_path = os.path.join(dir_path, 'Confusion_Matrix')
param_path = os.path.join(dir_path, 'truth_correspond.csv')

def mapping(vision_filename):
    video_ID = ''
    subject_ID = int(vision_filename[0:2])
    video_cut = vision_filename[-1]
    #print('video:', video_cut)
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
    truth, vision = ([] for i in range(2))
    reader_truth = csv.reader(open(os.path.join(truth_path, truth_filename + '.csv'), mode='r', encoding="utf-8-sig", errors="replace"))
    reader_vision = csv.reader(open(os.path.join(vision_path, vision_filename + '.csv'), mode='r', encoding="utf-8-sig", errors="replace"))
    for rowT, rowV in zip(reader_truth, reader_vision):
        truth.append(rowT)
        vision.append(rowV)
    return truth, vision

def writefile(accuracy, tpr, path):
    with open(os.path.join(path, 'table_line_acc.csv'), 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(accuracy)
    with open(os.path.join(path, 'table_line_tpr.csv'), 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(tpr)
    return


if __name__ == "__main__":
    vision_files = os.listdir(vision_path)
    mean_tpr = []
    for filename in vision_files:
        if filename != '.DS_Store' and filename != '.DS_Store.csv':
            #打散Video的名称, 每一个新的Video都有一个新的Directory, 根据S2或者S4分类
            print(filename)
            upper_limbs_truth, upper_limbs_vision, back_truth, back_vision = ([] for i in range(4))
            leg_truth, leg_vision, neck_truth, neck_vision = ([] for i in range(4))
            vision_filename = modify_filename(filename)
            vision_filename = vision_filename.replace('.csv', '')
            video_ID = vision_filename[3:7]
            video_path = os.path.join(output_path, video_ID)
            if not os.path.exists(video_path):
                os.makedirs(video_path)
            truth, vision = count_postureCode(vision_filename)
            read_length = int(len(vision)/6)
            if read_length > len(truth):
                read_length = len(truth)
            #新建一个Directory
            new_path = os.path.join(video_path, vision_filename + '_CM')
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            options = ['Upper Limb','Back','Knee','Neck']
            table_line_acc = []
            table_line_tpr = []
            for i in range(len(options)):
                print_stdout = sys.stdout
                out_file = open(os.path.join(new_path, options[i] + '_CM.txt'), 'w')
                sys.stdout = out_file
                con_matrix, tpr, labels, accuracy = confusion_matrix(truth, vision, i)
                print_confusion_matrix(con_matrix, labels, tpr, accuracy)
                if i == 2:
                    accuracy.remove(accuracy[1])
                    tpr.remove(tpr[1])
                table_line_acc.extend(accuracy)
                table_line_tpr.extend(tpr)
                sys.stdout = print_stdout
                out_file.close()
            sum_acc = sum_tpr = 0
            num_acc = num_tpr = 0
            for i in range(len(table_line_acc)):
                if table_line_acc[i] != 404:
                    sum_acc = sum_acc + table_line_acc[i]
                    num_acc = num_acc + 1
                if table_line_tpr[i] != 404:
                    sum_tpr = sum_tpr + table_line_tpr[i]
                    num_tpr = num_tpr + 1
            if num_acc != 0:
                table_line_acc.append(sum_acc / num_acc)
            if num_tpr != 0:
                table_line_tpr.append(sum_tpr / num_tpr)
                mean_tpr.append([vision_filename, sum_tpr / num_tpr])
                print(vision_filename, sum_tpr / num_tpr)
            table_line_acc[8], table_line_acc[9] = table_line_acc[9], table_line_acc[8]
            table_line_tpr[8], table_line_tpr[9] = table_line_tpr[9], table_line_tpr[8]
            writefile(table_line_acc, table_line_tpr, new_path)
    with open(os.path.join(output_path, 'mean_tpr.csv'), 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(mean_tpr)
