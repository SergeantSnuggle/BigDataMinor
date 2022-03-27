import pandas as pd

import database as db

# df = pd.read_csv("Hotel_Reviews.csv", sep=',', engine='python', on_bad_lines='warn')
#
# db.insert_df_into_db(df, "rawhoteldata")

db1 = db.retrive_table_into_df("rawhoteldata")
