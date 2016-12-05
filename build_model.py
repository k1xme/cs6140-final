import random
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
import numpy as np
import pymongo

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


def main():
    client = pymongo.MongoClient()
    db = client.yelp_data
    data = db.formatted_data
    cursor = data.find({})

    training_data = []
    training_label = []
    test_data = []
    test_label = []

    for document in cursor:
        document.pop("_id")
        document.pop("business_id")
        label = document.pop("Success")

        if random.random() < 0.8:
            training_data.append(document)
            training_label.append(label)
        else:
            test_data.append(document)
            test_label.append(label)

    vec = DictVectorizer()
    X = vec.fit_transform(training_data).toarray()
    X = StandardScaler().fit_transform(X)
    y = np.array(training_label)

    test_X = vec.fit_transform(test_data).toarray()
    test_X = StandardScaler().fit_transform(test_X)
    test_y = np.array(test_label)

    classifiers = [
        #  KNeighborsClassifier(3),
        #  SVC(kernel="linear", C=0.025),
        #  SVC(gamma=2, C=1),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1),
        AdaBoostClassifier(),
        GaussianNB()]
    for clf in classifiers:
        clf.fit(X, y)
        predict_y = clf.predict(test_X)
        print accuracy_score(test_y, predict_y)


if __name__ == '__main__':
    main()