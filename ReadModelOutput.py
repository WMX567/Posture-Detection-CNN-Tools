"""
Read CNN results (txt files)
wumengxi@umich.edu
"""
import os

def read_model_output(input_file):
    X, Y, video_frames = ([] for i in range(3))
    file = open(input_file, encoding='utf-8', errors='replace')
    lines = [line.strip('\n') for line in file]
    lines.pop(0)
    for line in lines:
        line = line.split()
        video_frames.append(line[0])
        line.pop(0)
        values = [float(s) for s in line if s != '']
        row_X, row_Y = ([] for i in range(2))
        for i in range(len(values)):
            if i % 2 == 0:
                row_X.append(values[i])
            else:
                row_Y.append(values[i])
        X.append(row_X)
        Y.append(row_Y)
    return X, Y, video_frames
