"""
Sample the posture codes calculated from CNN output to match the groud truth file
wumengxi@umich.edu
"""
import os,csv
import pandas as pd

file_path = '/Users/wumengxi/Desktop/Posture_Codes/'
output_path = '/Users/wumengxi/Desktop/Sample_Results'

posture_files = os.listdir(file_path)
for filename in posture_files:
	posture_codes = pd.read_csv(file_path + filename, encoding = 'utf8').dropna(how='all')
	posture_codes = posture_codes.values.tolist()
	posture_sampled = []
	read_length = int(len(posture_codes)/6)
	for i in range(read_length):
		posture_sampled.append(posture_codes[i*6])
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(posture_sampled)

