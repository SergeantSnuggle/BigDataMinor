import time
from datetime import datetime
from dask_ml.feature_extraction.text import HashingVectorizer
from dask_ml.wrappers import Incremental
from sklearn.linear_model import SGDClassifier
from dask_ml.model_selection import train_test_split
import dask.array as da
import dask.dataframe as ddf
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, auc
from joblib import dump, load
import json
from matplotlib import pyplot as plt

from BDSE.individual_Assignment_2.mongodb.retrieveData import retrieve_longest_reviews
from BDSE.individual_Assignment_2.data.cleaning import dask_preprocessing, preprocess_reviews


def build_model():
    reviews = retrieve_longest_reviews()

    daskReviews = dask_preprocessing(reviews)

    start = time.time()

    vect = HashingVectorizer()

    model = Incremental(SGDClassifier(penalty="l2", loss='modified_huber', alpha=0.1), scoring="accuracy",
                        assume_equal_chunks=True)

    X = vect.fit_transform(daskReviews["review"])
    y = daskReviews["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=69)

    # get unique fields from y_train (0 and 1)
    classes = da.unique(y_train).compute()

    model.fit(X_train, y_train, classes=classes)
    duration = round(time.time() - start)

    print(duration)

    predictions = model.predict(X_test)
    print(accuracy_score(y_test, predictions))

    dump(model, 'daskmodel.joblib')
    dump(vect, 'daskcv.sav')

    additional_model_values = {
        'accuracy': round(accuracy_score(y_test, model.predict(X_test)), 3),
        'auc': round(roc_auc_score(y_test, model.predict_proba(X_test)[::, 1]), 3),
        'date': str(datetime.now().replace(microsecond=0)),
        'duration': duration,
        'amount_of_reviews': len(daskReviews)
    }

    json_additional_model_values = json.dumps(additional_model_values)

    with open('daskValues.json', 'w') as file:
        file.write(json_additional_model_values)
    file.close()

    name = 'Incremental SGDClassifier'
    probability = model.predict_proba(X_test)
    predidions = probability[:, 1]
    fpr, tpr, threshold = roc_curve(y_test, predidions)
    roc_auc = auc(fpr, tpr)

    plt.title('ROC curve ' + name)
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.savefig('daskModel.png')
    plt.close()


def live_predict_dask(review):
    model = load('daskmodel.joblib')
    vect = load('daskcv.sav')

    process_review = preprocess_reviews([review])

    vectReview = vect.transform(process_review)

    prediction = model.predict(vectReview)

    return prediction


def get_dask_results():
    file = open('daskValues.json')
    results = file.read()
    json_results = json.loads(results)

    return json_results


if __name__ == "__main__":
    #build_model()

    #test = live_predict_dask("I really hated this hotel. Its really dirty")

    test = get_dask_results()