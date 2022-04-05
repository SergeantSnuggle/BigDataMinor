import pandas as pd
from sklearn.model_selection import train_test_split

import BDSE.Individual_Assignment_1.database as db


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


def get_raw_data():
    dfKaggleReviews = pd.read_csv("data/Hotel_Reviews.csv")
    dfScrappedSelenium = pd.read_csv("data/scrappedrawtriphoteldata.csv")
    dfOwnReviews = pd.read_csv("data/own_reviews.csv")

    dfKaggleReviews["label"] = dfKaggleReviews['Reviewer_Score'].apply(lambda x: 1 if x > 5.5 else 0)
    dfOwnReviews["label"] = dfOwnReviews['review_score'].apply(lambda x: 1 if x > 5.5 else 0)

    dfReviews = pd.concat([dfKaggleReviews, dfScrappedSelenium, dfOwnReviews], ignore_index=True)
    dfReviews = dfReviews.sample(frac=1).reset_index(drop=True)

    return dfReviews