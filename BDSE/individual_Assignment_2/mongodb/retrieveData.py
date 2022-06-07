from pymongo import MongoClient
import pandas as pd

client = MongoClient("localhost:27017")
db = client.assignment2


def retrieve_all(collection):
    results = db[collection].find({}, {'_id': False})
    source = list(results)
    resultDf = pd.DataFrame(source)

    return resultDf


if __name__ == '__main__':
    all = retrieve_all()