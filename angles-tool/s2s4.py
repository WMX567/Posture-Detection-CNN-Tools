"""
S2_1 + S2_2 + S2_3 = S2
S4_1 + S4_2 + S4_3 = S4
wumengxi@umich.edu
"""
import os, csv

dir_path = os.path.dirname(os.path.realpath(__file__))
vision_path = os.path.join(dir_path, 'Files')
read_post = []
vision_files = os.listdir(vision_path)
name = ''
for filename in vision_files:
    if filename != '.DS_Store' and filename != '.DS_Store.csv':
        if filename != 's2s4.py':
            name = filename
            reader_truth = csv.reader(open(os.path.join(vision_path, name), encoding="utf-8-sig", errors="replace"))
            for row in reader_truth:
                read_post.append(row)

name = name.replace('.csv', '')
video_cut = name[-1]
name = name.replace('_'+ video_cut, '')
output_path = os.path.join(dir_path, name + '.csv')
with open(output_path, 'w') as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(read_post)

