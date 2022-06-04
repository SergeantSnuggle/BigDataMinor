# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
import pymongo
from pymongo import MongoClient
import pandas as pd
import ssl

uri='mongodb+srv://<user>:<password>@cluster0.hkfyo.mongodb.net/zipcode?retryWrites=true&w=majority'

client = MongoClient(uri)

db=client.zipcode

df=pd.read_csv("population.csv")

db.population.insert_many(df.to_dict('records'))

