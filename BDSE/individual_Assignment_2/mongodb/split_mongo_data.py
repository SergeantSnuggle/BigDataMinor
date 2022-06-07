from pymongo import MongoClient
import pandas as pd
import retrieveData as retrieve

client = MongoClient("localhost:27017")
db = client.assignment2

def insert_hotels(df):
    dfNoDupes = df.drop_duplicates(subset="Hotel_Name")
    dfHotels = dfNoDupes[['Hotel_Name', 'Hotel_Address', 'Total_Number_of_Reviews', 'Average_Score', 'lat', 'lng']]
    db.hotels.insert_many(dfHotels.to_dict('records'))


if __name__ == "__main__":
    result = retrieve.retrieve_all("hotels")
    # insert_hotels(result)