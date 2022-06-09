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


def retrieve_avg_nat():
    test = db.hotel_reviews_raw.aggregate([
        {"$group": {
            "_id": "$Reviewer_Nationality",
            "average_review_score": {
                "$avg": "$Reviewer_Score"
            }
        }
        }
    ])
    results = pd.DataFrame(list(test))
    results = results.rename(columns={'_id': 'nationality'})
    results['nationality'].replace(' ', np.nan, inplace=True)
    results.dropna(subset=['nationality'], inplace=True)
    return results


if __name__ == '__main__':
    avgNat = retrieve_avg_nat()