"""
   table.py
   Overall posture codes estimations summary
   BMI: Over Weight, Normal Weight, Underweight
   Views: Left, Right, Diag
   wumengxi@umich.edu
"""
import os,sys,csv
import numpy as np
from ReadModelOutput import modify_filename
from datasum import count_postureCode
from confmatrix import re_value, define_label, confusion_matrix, adjust_value_ver2


dir_path = os.path.dirname(os.path.realpath(__file__))
vision_path = os.path.join(dir_path, 'Right')
truth_path = os.path.join(dir_path, 'Ground_Truth')
output_path = os.path.join(dir_path, 'Confusion_Matrix')
param_path = os.path.join(dir_path, 'truth_correspond.csv')


def statistics(actual, pred, option):
    assert(len(actual) == len(pred))
    labels = define_label(option)
    matrix, labels = adjust_value_ver2(actual, pred, option)
    tpr, labels, accuracy = confusion_matrix(matrix, labels)
    return matrix, tpr, labels, accuracy


if __name__ == "__main__":
    print('vision path:', vision_path)
    vision_files = os.listdir(vision_path)
    mean_tpr = []
    elbow_truth, back_truth, knee_truth, neck_truth = [0]*10, [0]*4, [0]*2, [0]*2
    elbow_vision, back_vision, knee_vision, neck_vision = [0]*10, [0]*4, [0]*2, [0]*2
    elbow_T, back_T, knee_T, neck_T = ([] for i in range(4))
    elbow_V, back_V, knee_V, neck_V = ([] for i in range(4))
    for filename in vision_files:
        if filename != '.DS_Store' and filename != '.DS_Store.csv':
            print(filename)
            vision_filename = modify_filename(filename)
            print(vision_filename)
            vision_filename = vision_filename.replace('.csv', '')
            truth, vision = count_postureCode(vision_filename, vision_path)
            read_length = int(len(vision))
            if read_length > len(truth):
                read_length = len(truth)
            vision = [vision[i] for i in range(read_length)]
            truth = [truth[i] for i in range(read_length)]
            elbow_codes = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            back_codes = ['1', '4', '7', '9']
            knee_codes = ['0', '8']
            neck_codes = ['0', '1']
            elbow_t, back_t, knee_t, neck_t = ([] for i in range(4))
            elbow_v, back_v, knee_v, neck_v = ([] for i in range(4))
            read_length = len(vision)
            if len(vision) < len(truth):
                read_length = len(truth)
            for i in range(read_length):
                if truth[i][0] != '完':
                    elbow_t.append(truth[i][0])
                    elbow_v.append(vision[i][0])
                if truth[i][1] != '完':
                    back_t.append(truth[i][1])
                    back_v.append(vision[i][1])
                if truth[i][2] != '完':
                    knee_t.append(truth[i][2])
                    knee_v.append(vision[i][2])
                if truth[i][3] != '完':
                    neck_t.append(truth[i][3])
                    neck_v.append(vision[i][3])
            neck_v = ['1' if v=='2' else v for v in neck_v]
            neck_t = ['1' if t=='2' else t for t in neck_t]
            for i in range(len(back_codes)):
                for j in range(len(back_t)):
                    if back_t[j] == back_codes[i]:
                        back_truth[i] += 1
                    if back_v[j] == back_codes[i]:
                        back_vision[i] += 1
            for i in range(len(elbow_codes)):
                for j in range(len(elbow_t)):
                    if elbow_t[j] == elbow_codes[i]:
                        elbow_truth[i] += 1
                    if elbow_v[j] == elbow_codes[i]:
                        elbow_vision[i] += 1
            for i in range(len(knee_codes)):
                for j in range(len(knee_t)):
                    if knee_t[j] == knee_codes[i]:
                        knee_truth[i] += 1
                    if knee_v[j] == knee_codes[i]:
                        knee_vision[i] += 1
            for i in range(len(neck_codes)):
                for j in range(len(neck_t)):
                    if neck_t[j] == neck_codes[i]:
                        neck_truth[i] += 1
                    if neck_v[j] == neck_codes[i]:
                        neck_vision[i] += 1
            elbow_T.extend(elbow_t)
            elbow_V.extend(elbow_v)
            back_T.extend(back_t)
            back_V.extend(back_v)
            knee_T.extend(knee_t)
            knee_V.extend(knee_v)
            neck_T.extend(neck_t)
            neck_V.extend(neck_v)
    mean_acc = [0]*3
    matrix, elbow_tpr, labels, elbow_acc = statistics(elbow_T, elbow_V, 0)
    matrix, back_tpr, labels, back_acc =  statistics(back_T, back_V, 1)
    matrix, knee_tpr, labels, knee_acc =  statistics(knee_T, knee_V, 2)
    matrix, neck_tpr, labels, neck_acc =  statistics(neck_T, neck_V, 3)
    mean_acc[0] = np.sum(elbow_acc)/len(elbow_acc)
    mean_acc[1] = (np.sum(knee_acc) + np.sum(back_acc))/(len(back_acc) + len(knee_acc))
    mean_acc[2] = np.sum(neck_acc)/len(neck_acc)
    print('Elbow Truth:', elbow_truth)
    print('Elbow Vision:', elbow_vision)
    print('Back Truth:', back_truth)
    print('Back Vision:', back_vision)
    print('Knee Truth:', knee_truth)
    print('Knee Vision:', knee_vision)
    print('Neck Truth:', neck_truth)
    print('Neck Vision:', neck_vision)
    print('Elbow TPR', elbow_tpr)
    print('Back TPR', back_tpr)
    print('Knee TPR', knee_tpr)
    print('Neck TPR', neck_tpr)
    print('Elbow Acc', elbow_acc)
    print('Back Acc', back_acc)
    print('Knee Acc', knee_acc)
    print('Neck Acc', neck_acc)
    result = [elbow_truth, elbow_vision, elbow_acc, back_truth, back_vision, back_acc, 
              knee_truth, knee_vision, knee_acc, neck_truth, neck_vision, neck_acc, mean_acc]
    with open(os.path.join(output_path, 'All+result.csv'), 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(result)


