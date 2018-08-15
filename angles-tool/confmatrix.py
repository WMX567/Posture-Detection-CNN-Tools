"""
Confusion Matrix and TPR
wumengxi@umich.edu
"""
import numpy as np

def define_label(option):
	labels = []
	if option == 0:
		labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
	elif option == 1:
		labels = [1, 4, 7, 9]
	elif option == 2:
		labels = [0, 8]
	elif option == 3:
		labels = [0, 1] #2先不考虑
	return labels

def re_value(a, b):
	if a == 2:
		a = 1
	if b == 2:
		b = 1
	return a, b

def print_confusion_matrix(matrix, labels, tpr, accuracy):
	matrix = np.concatenate((np.array(labels)[:, None], matrix), axis = 1)
	labels = [str(label) for label in labels]
	labels = ['T/P'] + labels
	colwidth = max([len(label) for label in labels]+ [23])
	print("".join(item.ljust(colwidth) for item in labels))
	for row in matrix:
		row = [str(item) for item in row]
		print("".join(item.ljust(colwidth) for item in row))
	labels[0] = 'Labels:'
	tpr = [str(item) for item in tpr]
	tpr = ['TPR:'] + tpr
	accuracy = [str(item) for item in accuracy]
	accuracy = ['ACC:'] + accuracy
	print("".join(item.ljust(colwidth) for item in labels))
	print("".join(item.ljust(colwidth) for item in tpr))
	print("".join(item.ljust(colwidth) for item in accuracy))
	return

def confusion_matrix(actual, pred, option):
	assert(len(actual) == len(pred))
	labels = define_label(option)
	print(labels)
	matrix = np.zeros((len(labels),len(labels)), dtype=int)
	for act_line, pred_line in zip(actual, pred):
		print('act_line:', act_line)
		print('pred_line:', pred_line)
		if option == 3:
			act_line[3], pred_line[3] = re_value(int(act_line[3]), int(pred_line[3]))
		i = labels.index(int(act_line[option]))
		j = labels.index(int(pred_line[option]))
		matrix[i][j] = matrix[i][j] + 1
	#计算所需要的数值
	tpr = [0]*len(labels)
	accuracy = [0]*len(labels)
	total_sum = np.sum(matrix)
	row_sum = np.sum(matrix, axis=1)
	col_sum = np.sum(matrix, axis=0)
	for i in range(len(labels)):
		TP = matrix[i][i]
		FP = col_sum[i] - matrix[i][i]
		TN = total_sum - col_sum[i] - row_sum[i] + matrix[i][i]
		FN = row_sum[i] - matrix[i][i]
		tpr[i] = accuracy[i] = 404
		if TP + FN != 0:
			tpr[i] =  TP / (TP + FN)
		if TP + FN + FP + FN != 0:
			accuracy[i] = (TP + TN) / (TP + TN + FP + FN)
	return matrix, tpr, labels, accuracy

