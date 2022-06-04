import pymongo
from pymongo import MongoClient
import pandas as pd
import ssl

uri='mongodb+srv://<user>:<password>@cluster0.hkfyo.mongodb.net/zipcode?retryWrites=true&w=majority'

client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

database = client["zipcode"]
collection = database["population"]

query = {}

query["state"] = u"AR"

cursor = collection.find(query)
try:
    for doc in cursor:
        print(doc)
finally:
    client.close()