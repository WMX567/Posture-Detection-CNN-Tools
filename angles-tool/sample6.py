"""
Sample the posture codes to match the groud truth file
wumengxi@umich.edu
"""
import os,csv
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path,'PostureCodes')
output_path = os.path.join(dir_path,'Sample_Results')

posture_files = os.listdir(file_path)
for filename in posture_files:
	posture_codes = pd.read_csv(os.path.dirname(file_path, filename), encoding = 'utf8').dropna(how='all')
	posture_codes = posture_codes.values.tolist()
	posture_sampled = []
	read_length = int(len(posture_codes)/6)
	for i in range(read_length):
		posture_sampled.append(posture_codes[i*6])
		writer = csv.writer(output, lineterminator='\n')
		writer.writerows(posture_sampled)

		
		
