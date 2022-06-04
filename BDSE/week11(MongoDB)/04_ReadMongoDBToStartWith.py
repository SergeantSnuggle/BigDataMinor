
from pymongo import MongoClient
import pandas as pd

client = MongoClient("localhost:27017")

db=client.zipcode

# // SELECT * 
# // FROM zipcodes
result=db.population.find({})
#print(result)
source=list(result)
resultDf=pd.DataFrame(source)
resultDf.head


# // SELECT COUNT(*) 
# // FROM zipcodes

result=db.population.count_documents({})
print(result)

# // SELECT COUNT(*) 
# // FROM zipcodes
# // WHERE STATE=’AR’

filter = {"state":"AR"}
result = db.population.count_documents(filter)
print(result)

# // SELECT city, pop 
# // FROM zipcodes
# // WHERE STATE=’AR’

filter={"state":"AR"}
projection= { 
            "city" : "$city", 
            "pop" : "$pop",
             "_id" : int(0)
            }
result = db.population.find(filter, projection)
source = list(result)
resultDf = pd.DataFrame(source)

