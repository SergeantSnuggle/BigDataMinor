import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import dask.dataframe as ddf
import time

from BDSE.individual_Assignment_2.mongodb.retrieveData import retrieve_all


def preprocess_reviews(reviews, dask):
    REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    NO_SPACE = ""
    SPACE = " "

    reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]

    if dask == 1:
        return reviews
    else:
        reviews = remove_stop_words(reviews)
        return reviews


def remove_stop_words(reviews):
    english_stop_words = stopwords.words('english')
    removed_stop_words = []
    addition_stop_words = ['hotel', 'room', 'breakfast', 'staff', 'rooms', 'location', 'u']
    for review in reviews:
        removed_stop_words.append(
            ' '.join([word for word in review.split()
                      if (word not in english_stop_words) and (word not in addition_stop_words)])
        )

    return removed_stop_words


def stem_text(reviews):
    stemmer = PorterStemmer()
    return [' '.join([stemmer.stem(word) for word in review.split()]) for review in reviews]


def clean_text_pandas(df):
    df["review"] = preprocess_reviews(df['review'], 0)
    df["review"] = remove_stop_words(df['review'])
    df["review"] = stem_text(df['review'])
    return df


def clean_text_dask(df):
    df["review"] = preprocess_reviews(df['review'], 1)
    return df


def dask_preprocessing(reviews):
    dask_dataframe = ddf.from_pandas(reviews, npartitions=6)
    result = dask_dataframe.map_partitions(clean_text_dask, meta=reviews)

    cleaned = result.compute()

    return cleaned


def get_dask_reviews():
    reviews = retrieve_all("labelled_reviews")
    daskReviews = dask_preprocessing(reviews)

    return daskReviews