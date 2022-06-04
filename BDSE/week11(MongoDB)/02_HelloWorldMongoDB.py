# https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
from pymongo import MongoClient

# connect to MongoDB, 
client = MongoClient("localhost:27017")
db = client.admin
client.list_database_names()

