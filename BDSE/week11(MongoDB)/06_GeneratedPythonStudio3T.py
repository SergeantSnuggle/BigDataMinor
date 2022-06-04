# Requires pymongo 3.6.0+
from pymongo import MongoClient

client = MongoClient("mongodb://host:port/")
database = client["zipcode"]
collection = database["population"]

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

query = {}

query["state"] = u"AR"

cursor = collection.find(query)
try:
    for doc in cursor:
        print(doc)
finally:
    client.close()
