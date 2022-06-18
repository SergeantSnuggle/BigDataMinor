from pymongo import MongoClient
import pandas as pd
import json
import numpy as np

client = MongoClient("localhost:27017")
db = client.assignment2


def retrieve_all(collection):
    results = db[collection].find({}, {'_id': False})
    source = list(results)
    resultDf = pd.DataFrame(source)

    return resultDf


def retrieve_unique_hotels(min_hotel_score=1):
    pipeline = [
        {
          "$match": {
              "Average_Score": {
                "$gte": int(min_hotel_score)
              }
          }
        },
        {
            "$project": {
                "lat": "$lat",
                "lng": "$lng",
                "Hotel_Name": "$Hotel_Name",
                "Hotel_Address": "$Hotel_Address",
                "Average_Score": "$Average_Score",
                "Total_Number_of_Reviews": "$Total_Number_of_Reviews",
                "_id": 0
            }
        },
        {
            "$group": {
                "_id": None,
                "distinct": {
                    "$addToSet": "$$ROOT"
                }
            }
        },
        {
            "$unwind": {
                "path": "$distinct",
                "preserveNullAndEmptyArrays": False
            }
        },
        {
            "$replaceRoot": {
                "newRoot": "$distinct"
            }
        }
    ]

    cursor = db.hotel_reviews_raw.aggregate(
        pipeline,
        allowDiskUse=True
    )
    result = pd.DataFrame(list(cursor))
    result = result[result['lat'].astype(str) != 'NA']
    result = result[result['lng'].astype(str) != 'NA']
    result[['lat', 'lng', 'Average_Score', 'Total_Number_of_Reviews']] = result[
        ['lat', 'lng', 'Average_Score', 'Total_Number_of_Reviews']].apply(pd.to_numeric)

    return result


def retrieve_avg_nat():
    avgNat = db.hotel_reviews_raw.aggregate([
        {"$group": {
            "_id": "$Reviewer_Nationality",
            "average_review_score": {
                "$avg": "$Reviewer_Score",
            },
            "amount_reviews": {
                "$sum": 1
            }
        }
        }
    ])
    results = pd.DataFrame(list(avgNat))
    results = results.rename(columns={'_id': 'nationality'})
    results['nationality'].replace(' ', np.nan, inplace=True)
    results.dropna(subset=['nationality'], inplace=True)
    results['average_review_score'] = round(results['average_review_score'], 2)
    return results


def retrieve_longest_reviews():
    #.sort('review_word_count', -1)
    pos = db.labelled_reviews.find({'label': 1}, {'_id': False}).limit(5000)
    posList = list(pos)
    posDf = pd.DataFrame(posList)

    neg = db.labelled_reviews.find({'label': 0}, {'_id': False}).limit(5000)
    negList = list(neg)
    negDf = pd.DataFrame(negList)

    allReviews = pd.concat([negDf, posDf], ignore_index=True)

    shuffleAll = allReviews.sample(frac=1)

    return shuffleAll


def retrieve_amount_reviews():
    amount = db.hotel_reviews_raw.count_documents({})

    return amount


def retrieve_amount_labelled(label):
    amount = db.labelled_reviews.count_documents({'label': label}, {})
    return amount


def retrieve_amount_hotels():
    amount = db.hotel_reviews_raw.distinct('Hotel_Name')
    amount = list(amount)
    amount = len(pd.DataFrame(amount))
    return amount


if __name__ == '__main__':
    #avgNat = retrieve_avg_nat()

    count = retrieve_avg_nat()
