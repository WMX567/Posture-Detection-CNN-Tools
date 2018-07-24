import matplotlib.pyplot as plt
import mayavi.mlab as m
import numpy as np
import csv

output_path = '/Users/wumengxi/Desktop/Output_3D_Plot/'
sensor_data_path = '/Users/wumengxi/Desktop/Raw_Data_Sensor/toyota_new_2017_05_14_144140_001_3d.csv'
index_path = '/Users/wumengxi/Desktop/3D_Angles/index_ref.csv'

x, y, z, index_ref = ([] for i in range(4))
with open(sensor_data_path, encoding='utf-8', errors='replace') as csvfile:
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

with open(index_path, encoding='utf-8', errors='replace') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        index_ref.append(row)

for i in range(20):
    X, Y, Z = ([] for i in range(3))
    left_arm = [x[i][5]-x[i][4], y[i][5]-y[i][4], z[i][5]-z[i][4]]
    print(left_arm)
    right_arm = [x[i][11]-x[i][10], y[i][11]-y[i][10], z[i][11]-z[i][10]]
    print(right_arm)
    left_shoulder = [x[i][4]-x[i][3], y[i][4]-y[i][3], z[i][4]-z[i][3]]
    print(left_shoulder)
    right_shoulder = [x[i][10]-x[i][9], y[i][10]-y[i][9], z[i][10]-z[i][9]]
    print(right_shoulder)
    left_knee = [x[i][1]-x[i][2], y[i][1]-y[i][2], z[i][1]-z[i][2]]
    print(left_knee)
    right_knee = [x[i][13]-x[i][12], y[i][13]-y[i][12], z[i][13]-z[i][12]]
    print(right_knee)
    head = [x[i][8]-x[i][7], y[i][8]-y[i][7], z[i][8]-z[i][7]]
    print(head)
    back = [(x[i][3]+x[i][9]-x[i][0]-x[i][12])/2, (y[i][3]+y[i][9]-y[i][0]-y[i][12])/2, (z[i][3]+z[i][9]-z[i][0]-z[i][12])/2]
    print(back)
    fig = plt.figure()
    origin = [0, 0, 0]
    X, Y, Z = zip(origin, origin, origin, origin, origin, origin, origin, origin)
    U, V, W = zip(left_arm, right_arm, left_shoulder, right_shoulder, left_knee, right_knee, head, back)
    """X = [left_arm[0], right_arm[0], left_shoulder[0], right_shoulder[0], left_knee[0], right_knee[0], head[0], back[0]]
    Y = [left_arm[1], right_arm[1], left_shoulder[1], right_shoulder[1], left_knee[1], right_knee[1], head[1], back[1]]
    Z = [left_arm[2], right_arm[2], left_shoulder[2], right_shoulder[2], left_knee[2], right_knee[2], head[2], back[2]]"""
    m.quiver3d(X,Y,Z,U,V,W)
    plt.savefig(output_path + str(i)+'graph.png')


