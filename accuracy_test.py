import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, \
       confusion_matrix, \
        accuracy_score

from sklearn import model_selection
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

k = 4
k_range = range(1,26)
scores = {}
scores_list = []

# prepare configuration for cross validation test harness
# seed = 100

balance_data = pd.read_csv('datasets/dataset.new.csv',header=None)
#print(balance_data)

# Feature set
X = balance_data.values[:, 1:7]
#print(X)
# print(X.shape)
# print(X)
# Target set
Y = balance_data.values[:, 0]
#print(Y)
# Y = dataset('Class')

# Split data
X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.2, random_state=100)

# classifier

nb_clf = GaussianNB().fit(X_train, Y_train)
Y_pred = nb_clf.predict(X_test)
score = metrics.accuracy_score(Y_test, Y_pred)
print(score)

for k in k_range:
    clf = KNeighborsClassifier(n_neighbors = k).fit(X_train, Y_train)
    Y_pred = clf.predict(X_test)
    scores[k] = metrics.accuracy_score(Y_test,Y_pred)
    print("k= {} \t {}".format(k, scores[k]))
    scores_list.append(metrics.accuracy_score(Y_test,Y_pred))



#kfold = model_selection.KFold(n_splits=10, random_state=seed)
#scoring = 'accuracy'

#cv_results = model_selection.cross_val_score(clf, X, Y, cv=kfold, scoring=scoring)


# Xnew = [[7380, 204, 14644, 69, -117, 191]]

#data_unclassified = pd.read_csv('new_data.csv', header=None)

#print("unclass: \n{}\n{}".format(data_unclassified,type(data_unclassified)))


#f = open("result.txt", "w")
#f.write(y_pred[0])
#print(y_pred)
