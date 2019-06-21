import pandas as pd
from sklearn import model_selection
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

class Classifier():
    __result = None
    __algorithm = None
    __dataset = None
    __clf = None
    __dataset_x = None
    __dataset_y = None

    def __init__(self, algorithm, dataset = "datasets/dataset.csv"):
        self.__algorithm = algorithm

        self.__dataset = pd.read_csv(dataset, header=None)

        self.__dataset_x = self.__dataset.values[:, 1:7]
        self.__dataset_y = self.__dataset.values[:, 0]

        if self.__algorithm == "knn":
            self.__clf = KNeighborsClassifier(n_neighbors=4).fit(self.__dataset_x,self.__dataset_y)
        elif self.__algorithm == "nb":
            self.__clf =  GaussianNB().fit(self.__dataset_x,self.__dataset_y)

    def classify(self, data):
        self.__result = self.__clf.predict(pd.DataFrame(data).T)
        return(self.__result[0])