"""
Calculate the 3D angles
"""
import os, csv
import numpy as np
from ReadModelOuput import read_model_output
from Angle_3D_Cal import proccess_3D_angles

param_path = '/Users/wumengxi/Desktop/Sync_Diag_Parameters_Summary.csv'
sensor_data_path = '/Users/wumengxi/Desktop/Raw_Data_Sensor/'
output_path = '/Users/wumengxi/Desktop/3D_Angles/'
input_path = '/Users/wumengxi/Desktop/Final_Diag_NoTape/'
sensor_files = ['toyota_2017_05_28_135905_001_3d.csv']
files = ['FinalSkeleton_20_Diag_0133_S2.txt','FinalSkeleton_20_Diag_0133_S4.txt']
filenum = '133'

def read_linearRegression_parameters(filenum):
    lr_param = []
    with open(param_path, encoding='utf-8', errors='replace') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Video ID'] == filenum:
                lr_param = [float(row['Slope']),float(row['Intercept'])]
                break
    return lr_param

def data_selection(sensor_data_path, lr_param):
    x, y, z, X, Y, video_frames = ([] for i in range(6))
    #Read CNN estimation
    for inputfile in files:
        X_part, Y_part, video_frame = read_model_output(input_path + inputfile)
        X.extend(X_part)
        Y.extend(Y_part)
        video_frames.extend(video_frame)
    #Read Sensor data
    for filename in sensor_files:
        with open(sensor_data_path + filename, encoding='utf-8', errors='replace') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                x_temp, y_temp, z_temp = ([] for i in range(3))
                for i in range(0,15):
                    if row['Marker_'+str(i+1)+' x'] != '':
                        row['Marker_'+str(i+1)+' x'] = float(row['Marker_'+str(i+1)+' x'])
                    if row['Marker_'+str(i+1)+' y'] != '':
                        row['Marker_'+str(i+1)+' y'] = float(row['Marker_'+str(i+1)+' y'])
                    if row['Marker_'+str(i+1)+' z'] != '':
                        row['Marker_'+str(i+1)+' z'] = float(row['Marker_'+str(i+1)+' z'])
                    x_temp.append(row['Marker_'+str(i+1)+' x'])
                    y_temp.append(row['Marker_'+str(i+1)+' y'])
                    z_temp.append(row['Marker_'+str(i+1)+' z'])
                x.append(x_temp)
                y.append(y_temp)
                z.append(z_temp)
    x_final, y_final, z_final, index_ref = ([] for i in range(4))
    for i in range(len(video_frames)):
        index_match = int(lr_param[0] * video_frames[i][0] + lr_param[1])
        x_final.append(x[index_match-1])
        y_final.append(y[index_match-1])
        z_final.append(z[index_match-1])
        index_ref.append([index_match-1])
    with open(output_path + 'video_frames.csv', 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(video_frames)
    with open(output_path + 'index_ref.csv', 'w') as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(index_ref)
    return x_final, y_final, z_final, X, Y

def replace_invalid_data(x, y, z, is_2D):
    for i in range(len(x)):
        for j in range(len(x[i])):
            if x[i][j] == '':
                x[i][j] = -4111
            if y[i][j] == '':
                y[i][j] = -4111
            if is_2D == False and z[i][j] == '':
                z[i][j] = -4111
            elif is_2D == True:
                z[i][j] = 0
    return x, y, z

def cnn_sensor_diff_evaluation(lr_param, is_record):
    angle_3D_cal, angle_3D_truth, vectors_cal, vectors_truth = ([] for i in range(4))
    mean_diff = [0]*5
    num_values_used = [0]*5
    x, y, z, X, Y = data_selection(sensor_data_path, lr_param)
    x, y, z = replace_invalid_data(x, y, z, True)
    for i in range(0,len(X)):
        print('Frame:', i)
        angles, vectors = proccess_3D_angles(X[i], Y[i], z[i], False)
        angle_3D_cal.append(angles)
        vectors_cal.append(vectors)
        angles, vectors = proccess_3D_angles(x[i], y[i], z[i], True)
        angle_3D_truth.append(angles)
        vectors_truth.append(vectors)
    print('Length of X:', len(X))
    for i in range(len(angle_3D_truth)):
        for j in range(5):
            if angle_3D_truth[i][j] != -4111:
                mean_diff[j] = mean_diff[j] + np.absolute(angle_3D_cal[i][j] - angle_3D_truth[i][j])
                num_values_used[j] = num_values_used[j] + 1
    if is_record == True:
        with open(output_path + 'cal.csv', 'w') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(angle_3D_cal)
        with open(output_path + 'truth.csv', 'w') as output:
            writer = csv.writer(output, lineterminator='\n')
            writer.writerows(angle_3D_truth)
        for i in range(len(num_values_used)):
            print('Retrieve Rate:', num_values_used[i]/len(angle_3D_truth))
    return mean_diff, num_values_used

if __name__ == "__main__":
    lr = read_linearRegression_parameters(filenum)
    print('linear parameter:', lr)
    mean_diff, num_values_used = cnn_sensor_diff_evaluation(lr, True)
    for i in range(len(num_values_used)):
        mean_diff[i] = mean_diff[i] / num_values_used[i]
    print('Angle Accuracy:')
    print(mean_diff)
   """for i in range(-5, 5):
        for j in range(-5, 5):
            lr_param = [lr[0]+i*0.01, lr[1]+j*5]
            mean_diff, num_values_used = cnn_sensor_diff_evaluation(lr_param, False)
            meanDiffs.append(mean_diff)
            num_used.append(num_values_used)
    for i in range(len(num_used)):
        for j in range(len(num_used[i])):
            meanDiffs[i][j] = meanDiffs[i][j] / num_used[i][j]
    means = [np.mean(angles) for angles in meanDiffs]
    print('Means', means)
    minPos = means.index(min(means))
    print('Min Position:', minPos)
    best_fit_param = [lr[0]+minPos*0.01, lr[1]+minPos*5]"""








