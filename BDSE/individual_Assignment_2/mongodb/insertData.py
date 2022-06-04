import pymongo
import pandas as pd
from pymongo import MongoClient

# read csv
filename = 'Hotel_Reviews.csv'
df = pd.read_csv(filename)

# create connection with mongo


mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")


db = mongo_client["assignment2"]

hotel_review = db["hotel_reviews"]
hotel_review.insert_many(df.to_dict(orient='records'))

db_list = MongoClient().list_database_names()

if "assignment2" in db_list:
    print(db['hotel_reviews'].estimated_document_count())

    query = {"Reviewer_Nationality": {"$eq": " Poland "}, "Hotel_Name": {"$eq": "Hotel Arena"}}

    data = pd.DataFrame(list(db['hotel_reviews'].find(query)))
    print(data)
