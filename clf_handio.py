import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

from sklearn import model_selection
from sklearn.model_selection import learning_curve
# from sklearn.metrics import explained_variance_score, make_scorer

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.ensemble import VotingClassifier
from matplotlib.ticker import FuncFormatter

# prepare configuration for cross validation test harness
seed = int(round(time.time() * 1000))

balance_data = pd.read_csv('datasets/dataset.new.csv',
                           sep=',',
                           header=None)

# Feature set
X = balance_data.values[:, 1:6]
# Target set
Y = balance_data.values[:, 0]
# Y = dataset('Class')

# prepare models
models = []
models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC(gamma='scale')))
models.append(('ADB', AdaBoostClassifier()))
models.append(('RFC', RandomForestClassifier(n_estimators=100)))
models.append(('ETC', ExtraTreesClassifier(n_estimators=100)))
models.append(('GBC', GradientBoostingClassifier()))


"""
X_train, X_test, y_train, y_test = train_test_split(X, Y,
test_size=0.3,
random_state=100)
"""

# evaluate each model in turn
results = []
names = []
cv_means = []
kfold = model_selection.KFold(n_splits=10, random_state=seed)
scoring = 'accuracy'
for name, model in models:
    cv_results = model_selection.cross_val_score(model, X, Y,
                                                 cv=kfold,
                                                 scoring=scoring)
    results.append(cv_results)
    names.append(name)
    cv_means.append(cv_results.mean())
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)


"""
learning curve for best results from models
"""
# size_data = len(X)
# print(size_data)
# cv_fold = model_selection.KFold(size_data, shuffle=True)

call_models = dict(models)
cfl = call_models[names[pd.Series(cv_means).idxmax()]]
# cfl = AdaBoostClassifier()
train_sizes, train_scores, test_scores = learning_curve(cfl,
                                                        X, Y,
                                                        n_jobs=-1,
                                                        cv=kfold,
                                                        train_sizes=np.linspace
                                                        (.1, 1.0, 5),
                                                        verbose=0)

train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.subplots_adjust(hspace=0.8)


"""
boxplot algorithm comparison
"""

ax1.set_title('Comparação dos algoritmos')
ax1.boxplot(results)
ax1.set_xticklabels(names)

ax2.set_title(names[pd.Series(cv_means).idxmax()])
ax2.legend(loc="best")
ax2.set_xlabel("Tamaho do dataset")
ax2.set_ylabel("Acurácia")
ax2.invert_yaxis()

# box-like grid
ax2.grid()

# plot the std deviation as a transparent range at each training set size
ax2.fill_between(train_sizes,
                 train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std,
                 alpha=0.1,
                 color="r")

ax2.fill_between(train_sizes,
                 test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std,
                 alpha=0.1,
                 color="g")

# plot the average training and test score lines at each training set size
ax2.plot(train_sizes,
         train_scores_mean,
         'o-',
         color="r",
         label="Pontuação de treino")

ax2.plot(train_sizes,
         test_scores_mean,
         'o-',
         color="g",
         label="Cross-Validação")

ax2.annotate("%.1f%%" % (train_scores_mean[-1] * 100),
             xy=(train_sizes[-1], train_scores_mean[-1]),
             xytext=(5, 0), textcoords='offset points', va='center')

ax2.annotate("%.1f%%" % (test_scores_mean[-1] * 100),
             xy=(train_sizes[-1], test_scores_mean[-1]),
             xytext=(5, 0), textcoords='offset points', va='center')

# sizes the window for readability and displays the plot
# shows error from 0 to 1.1
ax2.set_ylim(-.1, 1.1)
ax2.set_xlim(0, train_sizes[-1] + 15)
ax2.set_xlabel("Tamanho do dataset")
ax2.set_xticks(train_sizes)
ax2.set_ylabel("Acurácia")
ax2.legend(loc="best")
ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y))) 
plt.show()