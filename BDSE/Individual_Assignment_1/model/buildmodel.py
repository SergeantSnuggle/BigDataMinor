from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix,  roc_auc_score
import pandas as pd
from BDSE.Individual_Assignment_1.buildData import get_build_data


def build_svm():
    X_train, X_test, y_train, y_test = get_build_data()

    vect = CountVectorizer(max_features=1000)
    X_train_vect = vect.fit_transform(X_train)
    X_test_vect = vect.transform(X_test)

    svm = SVC(probability=True, kernel='linear', gamma=0.1, C=0.01)

    svm.fit(X_train_vect, y_train)

    y_pred = svm.predict(X_test_vect)
    y_prob = svm.predict_proba(X_test_vect)[::, 1]

    print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("AUC: \n", roc_auc_score(y_test, y_prob))

    return svm


def build_mnb():
    X_train, X_test, y_train, y_test = get_build_data()

    vect = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X_train_vect = vect.fit_transform(X_train)
    X_test_vect = vect.transform(X_test)

    mnb = MultinomialNB(alpha=0.1, fit_prior=True)

    mnb.fit(X_train_vect, y_train)

    y_pred = mnb.predict(X_test_vect)
    y_prob = mnb.predict_proba(X_test_vect)[::, 1]

    print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("AUC: \n", roc_auc_score(y_test, y_prob))

    return mnb


def build_random():
    X_train, X_test, y_train, y_test = get_build_data()

    vect = CountVectorizer(max_features=1000)

    X_train_vect = vect.fit_transform(X_train)
    X_test_vect = vect.transform(X_test)

    randomForest = RandomForestClassifier(n_estimators=721,
                                          min_samples_split=2,
                                          min_samples_leaf=4,
                                          max_depth=75,
                                          criterion="gini",
                                          bootstrap=True,
                                          n_jobs=4)
    randomForest.fit(X_train_vect, y_train)

    y_pred = randomForest.predict(X_test_vect)
    y_prob = randomForest.predict_proba(X_test_vect)[::, 1]

    print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("AUC: \n", roc_auc_score(y_test, y_prob))

    return randomForest


def build_lr():
    X_train, X_test, y_train, y_test = get_build_data()

    vect = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X_train_vect = vect.fit_transform(X_train)
    X_test_vect = vect.transform(X_test)

    lr = LogisticRegression(solver='newton-cg', penalty='l2', C=100)

    lr.fit(X_train_vect, y_train)

    y_pred = lr.predict(X_test_vect)
    y_prob = lr.predict_proba(X_test_vect)[::, 1]

    print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("AUC: \n", roc_auc_score(y_test, y_prob))

    return lr