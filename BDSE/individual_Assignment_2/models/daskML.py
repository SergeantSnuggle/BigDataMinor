import time
from dask_ml.feature_extraction.text import HashingVectorizer
from dask_ml.wrappers import Incremental
from sklearn.linear_model import SGDClassifier
from dask_ml.model_selection import train_test_split
import dask.array as da
import dask.dataframe as ddf
from sklearn.metrics import accuracy_score
from joblib import dump, load

from BDSE.individual_Assignment_2.mongodb.retrieveData import retrieve_all
from BDSE.individual_Assignment_2.data.cleaning import dask_preprocessing


def build_dask_ml():
    reviews = retrieve_all("labelled_reviews")

    daskReviews = dask_preprocessing(reviews)

    start = time.time()

    vect = HashingVectorizer()

    model = Incremental(SGDClassifier(penalty="l2", loss='modified_huber', alpha=0.1), scoring="accuracy",
                        assume_equal_chunks=True)

    X = vect.fit_transform(daskReviews["review"])
    y = daskReviews["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42)

    # get unique fields from y_train (0 and 1)
    classes = da.unique(y_train).compute()

    model.fit(X_train, y_train, classes=classes)
    duration = round(time.time() - start)

    print(duration)

    predictions = model.predict(X_test)
    print(accuracy_score(y_test, predictions))

    dump(model, 'daskmodel.joblib')
    dump(vect, 'daskcv.sav')