from confmatrix import confusMatrix

actual = [[0,1, 2, 0], [1, 2, 3, 1], [0, 2, 1, 1], [4, 1, 2, 2], [1, 2, 3, 0]]
pred = [[2, 1, 3, 0], [1, 3, 2, 1], [1, 0, 0, 2], [2, 1, 0, 0], [1, 1, 2, 0]]
conmat, tpr, labels = confusMatrix(actual, pred, 3)
print(conmat)
print(labels)
print(tpr)
