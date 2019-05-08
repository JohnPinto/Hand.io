import pandas as pd
import serial

# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import classification_report, \
#        confusion_matrix, \
#        accuracy_score

from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier

portPath = "/dev/ttyACM1"
baud = 57600

# prepare configuration for cross validation test harness
seed = 100

balance_data = pd.read_csv('handio_data.csv',
                           sep=',',
                           header=None)

# Feature set
X = balance_data.values[:, 1:7]
# print(X.shape)
# print(X)
# Target set
Y = balance_data.values[:, 0]
# Y = dataset('Class')

# Split data
X_train, X_test, y_train, y_test = model_selection.train_test_split(
    X, Y,
    test_size=0.3,
    random_state=100)

# classifier
clf = KNeighborsClassifier()

kfold = model_selection.KFold(n_splits=10, random_state=seed)
scoring = 'accuracy'

cv_results = model_selection.cross_val_score(clf, X, Y,
                                             cv=kfold,
                                             scoring=scoring)

clf.fit(X_train, y_train)

# Xnew = [[7380, 204, 14644, 69, -117, 191]]

data_unclassified = pd.read_csv('new_data.csv',
                                   sep=',',
                                   header=None)

y_pred = clf.predict(data_unclassified)

f = open("result.txt", "w")
f.write(y_pred[0])
print(y_pred)
