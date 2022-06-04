
from pymongo import MongoClient
import pandas as pd

client = MongoClient("localhost:27017")

db=client.zipcode

# // SELECT COUNT(*) 
# // FROM zipcodes

result=db.population.count_documents({})
print(result)

# // SELECT COUNT(*) 
# // FROM zipcodes
# // WHERE STATE=’AR’

filter={"state":"AR"}
result=db.population.count_documents(filter)
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
result=db.population.find(  filter, projection)  
source=list(result)
resultDf=pd.DataFrame(source)

# // SELECT State, COUNT(*) as count
# // FROM zipcodes
# // GROUP BY State

group={ "$group" : {
                "_id" : {
                    "state" : "$state"
                }, 
                "Number" : {
                    "$sum" : int(1)
                }
            }
        }
project={"$project" : {
                        "state" : "$_id.state", 
                        "NumberOfCities" : "$Number", 
                        "_id" : int(0)
            }
        }
pipeline=[group,project]
result=db.population.aggregate(pipeline )  
source=list(result)
resultDf=pd.DataFrame(source)

# // SELECT State, COUNT(*) as count
# // FROM zipcodes
# // GROUP BY State
# // ORDER BY State DESC

sort={"$sort":{ "state":1}} 
#sort={"$sort":{"NumberOfCities":-1	}}

pipeline=[group,project,sort]
result=db.population.aggregate(pipeline )  
source=list(result)
resultDf=pd.DataFrame(source)

# // SELECT State, COUNT(*) as count
# // FROM zipcodes
# // GROUP BY State
# // HAVING (COUNT(*)>=100)
# // ORDER BY State DESC

match={"$match": {"NumberOfCities":{"$gte":int(1000)}}}

pipeline=[group,project,match, sort]
result=db.population.aggregate(pipeline )  
source=list(result)
resultDf=pd.DataFrame(source)

# // SELECT State, COUNT(city) as count
# // FROM zipcodes
# // WHERE State LIKE %N%
# // GROUP BY State
# // HAVING (COUNT(city)>=500)
# // ORDER BY State DESC

filter= { "$match" : {"state"  :{"$regex":".*N.*"}}} 
match={"$match": {"NumberOfCities":{"$gte":int(100)}}}

pipeline=[filter,group,project,match, sort]
result=db.population.aggregate(pipeline )  

source=list(result)
resultDf=pd.DataFrame(source)


#https://api.mongodb.com/python/2.0/examples/map_reduce.html

from bson.code import Code


map = Code("function () {emit(this.state, parseInt(1)); }" )
reduce=Code("function (key, values) { return Array.sum(values);}")

resultCol=db.population.map_reduce(map,reduce,"myresult") 
resultCol.find_one()

result=resultCol.find({})
source=list(result)
resultDf=pd.DataFrame(source)


map = Code("function () {emit(this.state, this.pop); }" )
reduce=Code("function (key, values) { return Array.sum(values);}")

resultCol=db.population.map_reduce(map,reduce,"myresult") 
result=resultCol.find({})
source=list(result)
resultDf=pd.DataFrame(source)



