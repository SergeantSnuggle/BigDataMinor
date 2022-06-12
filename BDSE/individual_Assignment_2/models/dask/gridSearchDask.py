from dask_ml.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from dask_ml.wrappers import Incremental
import sklearn.linear_model
import dask.dataframe as ddf
import pandas as pd

from BDSE.individual_Assignment_2.data.cleaning import get_dask_reviews

daskReviews = get_dask_reviews()

vect = HashingVectorizer()
X = vect.fit_transform(daskReviews["review"])
y = daskReviews["label"].astype(int)
est = sklearn.linear_model.SGDClassifier()
clf = Incremental(est, scoring='accuracy')
clf.fit(X, y, classes=[0, 1])

from sklearn.model_selection import GridSearchCV
param_grid = {"estimator__alpha": [0.1, 1.0, 10.0],
              "estimator__penalty": ['l2', 'l1', 'elasticnet'],
              "estimator__loss": ['hinge', 'modified_huber', 'log']}
gs = GridSearchCV(clf, param_grid)
gs.fit(X, y, classes=[0, 1])

results = pd.DataFrame(gs.cv_results_)