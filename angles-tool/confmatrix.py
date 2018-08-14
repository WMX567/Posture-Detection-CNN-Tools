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

def print_confusion_matrix(matrix, labels, tpr):
	matrix = np.concatenate((np.array(labels)[:, None], matrix), axis = 1)
	labels = [str(label) for label in labels]
	labels = ['T/P'] + labels
	colwidth = max([len(label) for label in labels]+ [10])
	print("".join(item.ljust(colwidth) for item in labels))
	for row in matrix:
		row = [str(item) for item in row]
		print("".join(item.ljust(colwidth) for item in row))
	print('True Positive Rate:')
	labels[0] = 'Labels:'
	tpr = [str(item) for item in tpr[0]]
	tpr = ['TPR:'] + tpr
	print("".join(item.ljust(colwidth) for item in labels))
	print("".join(item.ljust(colwidth) for item in tpr))
	return

def confusion_matrix(actual, pred, option):
	assert(len(actual) == len(pred))
	labels = define_label(option)
	matrix = np.zeros((len(labels),len(labels)), dtype=int)
	for i in range(len(labels)):
		for j in range(len(labels)):
			for act_line, pred_line in zip(actual, pred):
				if option == 3:
					act_line[3], pred_line[3] = re_value(act_line[3], pred_line[3])
				if act_line[option] == i and pred_line[option] == j:
					matrix[i][j] = matrix[i][j] + 1
	#计算所需要的数值
	tpr = np.zeros((1, len(labels)))
	for i in range(len(labels)):
		sum = np.sum(matrix[i])
		if sum != 0:
			tpr[0][i] = matrix[i][i]/sum
		else:
			tpr[0][i] = 404
	return matrix, tpr, labels

