import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

import database as db


def create_wordcloud(reviews):

    positiveReviews = reviews.loc[reviews['label'] == 1]
    negativeReviews = reviews.loc[reviews['label'] == 0]

    wordCloudPos = WordCloud(width=1000, height=1000).generate(' ' .join(positiveReviews['Review']))
    wordCloudNeg = WordCloud(width=1000, height=1000).generate(' ' .join(negativeReviews['Review']))

    plt.figure()
    plt.imshow(wordCloudPos, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    plt.figure()
    plt.imshow(wordCloudNeg, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    stopwords = set(STOPWORDS)
    wordCloudPosStop = WordCloud(width=1000, height=1000, stopwords=stopwords)\
        .generate(' '.join(positiveReviews['Review']))
    wordCloudNegStop = WordCloud(width=1000, height=1000, stopwords=stopwords)\
        .generate(' '.join(negativeReviews['Review']))

    plt.figure()
    plt.imshow(wordCloudPosStop, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    plt.figure()
    plt.imshow(wordCloudNegStop, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    stopwords.update(['hotel', 'room', 'breakfast', 'staff', 'rooms', 'location', 'u'])
    wordCloudPosStopUpdate = WordCloud(width=1000, height=1000, stopwords=stopwords)\
        .generate(' '.join(positiveReviews['Review']))
    wordCloudNegStopUpdate = WordCloud(width=1000, height=1000, stopwords=stopwords)\
        .generate(' '.join(negativeReviews['Review']))

    plt.figure()
    plt.imshow(wordCloudPosStopUpdate, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    plt.figure()
    plt.imshow(wordCloudNegStopUpdate, interpolation='bilinear')
    plt.axis('off')
    plt.show()

reviews = db.retrieve_table_into_df("cleanedhoteldata")
create_wordcloud(reviews)
