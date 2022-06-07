from pymongo import MongoClient
import pandas as pd


df=pd.read_csv("population.csv")

client = MongoClient("localhost:27017")

# Already existing database zipcode

db = client.zipcode

db.population.insert_many(df.to_dict('records'))
