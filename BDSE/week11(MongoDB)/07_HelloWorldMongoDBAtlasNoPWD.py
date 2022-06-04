# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
import pymongo
from pymongo import MongoClient
import pandas as pd
import ssl


# add user to database
# look at network access , whitelist some or all IP addresses
uri='mongodb+srv://<user>:<password>@cluster0.hkfyo.mongodb.net/zipcode?retryWrites=true&w=majority'

client = MongoClient(uri)

client.list_database_names()



