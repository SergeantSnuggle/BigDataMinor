import pandas as pd
from sqlalchemy import create_engine, inspect

engine = create_engine('mysql://root@localhost:3306/hotel_reviews')

def insert_df_into_db(df, table):
    """
    Insert a dataframe into the database hotel_reviews

    :param df: Dataframe to be inserted
    :param table: Name of table where data is to be inserted
    """
    print("Inserting data into database per 1000 chunks")
    df.to_sql(name=table, con=engine, if_exists='replace', index=False, chunksize=1000)


def retrieve_table_into_df(table):
    """
    Retrieves all data from a specified table and returns a dataframa

    :param table: The table you want to retrieve data from
    :return: returns a dataframe of retrieved data from the table
    """
    df = pd.read_sql("SELECT * FROM "+table, con=engine)
    return df

