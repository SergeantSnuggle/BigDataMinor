import pandas as pd
"Own made libraries"
import database as db
import scrapperSelenium
import scrapperSoup

# df = pd.read_csv("Hotel_Reviews.csv", sep=',', engine='python', on_bad_lines='warn')
#
# db.insert_df_into_db(df, "rawhoteldata")
#
#db1 = db.retrieve_table_into_df("rawhoteldata")
link = "https://www.tripadvisor.com/Hotel_Review-g14129477-d10426242-Reviews-HOSHINOYA_Tokyo-Otemachi_Chiyoda_Tokyo_Tokyo_Prefecture_Kanto.html"
scrappedReviews = scrapperSelenium.selenium_scrapper_tripadvisor(link, 20)
db.insert_df_into_db(scrappedReviews, "scrappedrawhoteldata")

df2 =db.retrieve_table_into_df("scrappedrawhoteldata")