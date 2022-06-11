import pymongo
import pandas as pd
from pymongo import MongoClient
from BDSE.individual_Assignment_2.mongodb.retrieveData import db, retrieve_all


def remove_redundant_reviews(review_df):
    minimum_words = 5
    review_df = review_df.loc[review_df.Review_Total_Positive_Word_Counts >= minimum_words]
    review_df = review_df.loc[review_df.Review_Total_Negative_Word_Counts >= minimum_words]

    return review_df


def label_reviews(review_df):
    df_pos = review_df.loc[:, ['Positive_Review', 'Review_Total_Positive_Word_Counts']]
    df_pos['label'] = 1

    df_neg = review_df.loc[:, ['Negative_Review', 'Review_Total_Negative_Word_Counts']]
    df_neg['label'] = 0

    df_pos = df_pos.rename({'Positive_Review': 'review', 'Review_Total_Positive_Word_Counts': 'review_word_count'}, axis=1)
    df_neg = df_neg.rename({'Negative_Review': 'review', 'Review_Total_Negative_Word_Counts': 'review_word_count'}, axis=1)

    combination_review = pd.concat([df_neg, df_pos], axis=0)

    shuffle_df = combination_review.sample(frac=1).reset_index(drop=True)

    return shuffle_df


if __name__ == '__main__':
    reviews = retrieve_all('hotel_reviews_raw')
    reviews = remove_redundant_reviews(reviews)
    reviews = label_reviews(reviews)

    db.labelled_reviews.insert_many(reviews.to_dict(orient='records'))