from confmatrix import confusion_matrix, print_confusion_matrix

actual = [[0,1, 2, 0], [1, 2, 3, 1], [0, 2, 1, 1], [4, 1, 2, 2], [1, 2, 3, 0]]
pred = [[2, 1, 3, 0], [1, 3, 2, 1], [1, 0, 0, 2], [2, 1, 0, 0], [1, 1, 2, 0]]
conmat, tpr, labels = confusion_matrix(actual, pred, 3)
print_confusion_matrix(conmat, labels, tpr)

