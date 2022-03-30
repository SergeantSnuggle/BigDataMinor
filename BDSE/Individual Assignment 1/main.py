import pandas as pd
from sklearn.model_selection import train_test_split

"Own made libraries"
import database as db
import scrapping.scrapperSelenium as scrapperSelenium
import scrapping.scrapperSoup as scrapperSoup
import textCleaning as tc


dfReviews = pd.read_csv("Hotel_Reviews.csv", sep=',')

dfStrippedReviews = tc.kaggle_strip_reviews(dfReviews)

dfLabelReviews = tc.kaggle_label_data(dfStrippedReviews)

X = dfLabelReviews["Review"]
y = dfLabelReviews["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

stemmedTrain = tc.get_stemmed_text(X_train)
stemmedTest = tc.get_stemmed_text(X_test)
db.insert_df_into_db(dfLabelReviews, "label_kaggle_reviews", "replace")

db.insert_df_into_db(dfReviews, "rawhoteldata", "replace")

db1 = db.retrieve_table_into_df("rawhoteldata")
link = "https://www.tripadvisor.com/Hotel_Review-g14129477-d10426242-Reviews-HOSHINOYA_Tokyo-Otemachi_Chiyoda_Tokyo_Tokyo_Prefecture_Kanto.html"
scrappedReviews = scrapperSelenium.selenium_scrapper_tripadvisor(link, 20)
db.insert_df_into_db(scrappedReviews, "scrappedrawhoteldata")

df2 =db.retrieve_table_into_df("scrappedrawhoteldata")
