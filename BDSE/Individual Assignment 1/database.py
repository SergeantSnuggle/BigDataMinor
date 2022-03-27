import pandas as pd
from sqlalchemy import create_engine, inspect

engine = create_engine('mysql://root@localhost:3306/hotel_reviews')

def insert_df_into_db(df, table):
    print("Inserting data into database per 1000 chunks")
    df.to_sql(name=table, con=engine, if_exists='replace', index=False, chunksize=1000)


def retrive_table_into_df(table):
    df = pd.read_sql("SELECT * FROM "+table, con=engine)
    return df

