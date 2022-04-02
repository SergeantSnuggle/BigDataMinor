import pandas as pd
from sklearn.model_selection import train_test_split

import database as db


def get_hyper_data():
    dfNegative = db.get_top_reviews(10000, 0)
    dfPositive = db.get_top_reviews(10000, 1)
    dfReviews = pd.concat([dfNegative, dfPositive], ignore_index=True)
    dfShuffled = dfReviews.sample(frac=1)
    X = dfShuffled["lemReviews"]
    y = dfShuffled["label"]

    return X, y


def get_build_data():
    df = db.retrieve_table_into_df("cleanedhoteldata")
    X = df['lemReviews']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=69)

    return X_train, X_test, y_train, y_test

