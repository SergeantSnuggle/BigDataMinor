from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

from BDSE.Individual_Assignment_1.buildData import get_hyper_data


def hyper_svm():
    X, y = get_hyper_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    vect = CountVectorizer(max_features=1000)
    X_train_vect = vect.fit_transform(X_train)

    kernels = ['linear', 'rbf', 'poly']
    cParams = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 10.0]
    gamma = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 10.0]

    random_grid = {'kernel': kernels,
                   'C': cParams,
                   'gamma': gamma}

    svm_base = SVC()
    svm_random = RandomizedSearchCV(estimator=svm_base,
                                    param_distributions=random_grid,
                                    n_iter=30,
                                    cv=5,
                                    verbose=2,
                                    random_state=42,
                                    n_jobs=4)

    svm_random.fit(X_train_vect, y_train)
    print(svm_random.best_params_)
    resultsDf = pd.DataFrame(svm_random.cv_results_)
    return resultsDf


def hyper_random():
    X, y = get_hyper_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    vect = CountVectorizer(max_features=1000)
    X_train_vect = vect.fit_transform(X_train)

    # Number of trees in random forest
    n_estimators = np.linspace(100, 3000, int((3000-100)/200) + 1, dtype=int)
    # Maximum number of levels in tree
    max_depth = [1, 5, 10, 20, 50, 75, 100, 150, 200]
    # Minimum number of samples required to split a node
    min_samples_split = [1, 2, 5, 10, 15, 20, 30]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 3, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # Criterion
    criterion=['gini', 'entropy']
    random_grid = {'n_estimators': n_estimators,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap,
                   'criterion': criterion}
    rf_base = RandomForestClassifier()
    rf_random = RandomizedSearchCV(estimator=rf_base,
                                   param_distributions=random_grid,
                                   n_iter=30,
                                   cv=5,
                                   verbose=2,
                                   random_state=42,
                                   n_jobs=4)
    rf_random.fit(X_train_vect, y_train)
    print(rf_random.best_params_)
    resultsDf = pd.DataFrame(rf_random.cv_results_)
    return resultsDf


def hyper_multiNB():
    X, y = get_hyper_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    vect = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X_train_vect = vect.fit_transform(X_train)

    mnb_base = MultinomialNB()
    alpha = [0, 0.1, 0.2, 0.5, 0.7, 1]
    fit_prior = [True, False]

    random_grid = {'alpha': alpha,
                   'fit_prior': fit_prior}

    mnb_random = RandomizedSearchCV(estimator=mnb_base,
                                    param_distributions=random_grid,
                                    n_iter=12,
                                    cv=5,
                                    verbose=2,
                                    random_state=42,
                                    n_jobs=4)

    mnb_random.fit(X_train_vect, y_train)
    print(mnb_random.best_params_)
    resultsDf = pd.DataFrame(mnb_random.cv_results_)
    return resultsDf


def hyper_lr():
    X, y = get_hyper_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=69)

    vect = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))

    X_train_vect = vect.fit_transform(X_train)

    lr_base = LogisticRegression()
    solvers = ['newton-cg', 'lbfgs', 'liblinear']
    penalty = ['l2']
    c_values = [100, 10, 1.0, 0.1, 0.01]

    random_grid = {'solver': solvers,
                   'penalty': penalty,
                   'C': c_values}

    lr_random = RandomizedSearchCV(estimator=lr_base,
                                   param_distributions=random_grid,
                                   n_iter=15,
                                   cv=5,
                                   verbose=2,
                                   random_state=42,
                                   n_jobs=4)

    lr_random.fit(X_train_vect, y_train)
    print(lr_random.best_params_)
    resultsDf = pd.DataFrame(lr_random.cv_results_)
    return resultsDf