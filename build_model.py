import random
import pymongo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score
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

    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM",
         "Decision Tree", "Random Forest", "Neural Net",
         "AdaBoost", "Naive Bayes"]

    classifiers = [
        KNeighborsClassifier(3),
        SVC(kernel="linear", C=0.025),
        SVC(gamma=2, C=1),
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        MLPClassifier(alpha=1),
        AdaBoostClassifier(),
        GaussianNB()]

    training_error = []
    test_error = []
    precision = []
    recall = []
    for name, clf in zip(names, classifiers):
        clf.fit(X, y)
        predict_y = clf.predict(test_X)
        train_e = 1 - accuracy_score(y, clf.predict(X))
        test_e = 1 - accuracy_score(test_y, predict_y)
        pre = precision_score(test_y, predict_y)
        rcl = recall_score(test_y, predict_y)
        print 'classifier: {} \ntraining error:{}\ntest error: {}\nprecsion: {}\nrecall: {}\n\n'.format(name, train_e, test_e, pre, rcl)

        training_error.append(train_e)
        test_error.append(test_e)
        precision.append(pre)
        recall.append(rcl)

    x_pos = np.arange(len(classifiers))
    ax = plt.subplot(111)
    rec1 = ax.bar(x_pos-0.3, training_error, width=0.2, align='center', color='green')
    rec2 = ax.bar(x_pos-0.1, test_error, width=0.2, align='center', color='blue')
    rec3 = ax.bar(x_pos+0.1, precision, width=0.2, align='center', color='red')
    rec4 = ax.bar(x_pos+0.3, recall, width=0.2, align='center', color='black')
    ax.legend((rec1[0], rec2[0], rec3[0], rec4[0]),
               ('Training Error', 'Test Error', 'Precision', 'Recall'))
    plt.show()

if __name__ == '__main__':
    main()
