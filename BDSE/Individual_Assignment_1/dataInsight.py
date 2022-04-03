import pandas as pd
from matplotlib import pyplot as plt

import buildData as build


def build_plots_reviews():
    dfReviews = build.get_raw_data()

    #reviews_per_hotel(dfReviews)
    amount_pos_neg(dfReviews)
    #average_score_nationality(dfReviews)


def reviews_per_hotel(dfReviews):
    dfReviews.drop_duplicates(inplace=True, subset=['Hotel_Name'])
    top_reviewed_hotels = dfReviews.nlargest(20, ['Total_Number_of_Reviews'])
    top_reviewed_hotels.plot.barh(x='Hotel_Name', y='Total_Number_of_Reviews', legend=False)
    plt.title('Top 20 hotels')
    plt.ylabel('Hotel')
    plt.xlabel('Number of reviews')
    plt.tight_layout()
    plt.savefig('dataInsight/top20hotels')


def amount_pos_neg(dfReviews):
    dfAmount = dfReviews['label'].value_counts()
    dfAmount.columns = ['label', 'amount']

    dfAmount.plot.bar()
    plt.title('Number of positives(1) and negatives(0)')
    plt.ylabel('Amount')
    plt.xlabel('Label')
    plt.tight_layout()
    plt.savefig('dataInsight/amount_pos_neg')


def average_score_nationality(dfReviews):
    dfScore = pd.DataFrame()
    dfScore['mean'] = dfReviews.groupby(["Reviewer_Nationality"])['Reviewer_Score'].mean()
    dfScore['amount'] = dfReviews['Reviewer_Nationality'].value_counts()
    dfScore = dfScore.sort_values(by='amount', ascending=False)
    dfScore = dfScore.head(10)
    dfScoreMean = dfScore['mean']

    dfScoreMean.plot.bar()
    plt.title('Average score per nationality sorted by most reviews')
    plt.ylabel('Average Score')
    plt.xlabel('Nationality')
    plt.tight_layout()
    plt.savefig('dataInsight/average_score')


build_plots_reviews()
