import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql://root@localhost:3306/hotel_reviews')


def insert_df_into_db(df, table, if_exists='append'):
    """
    Insert a dataframe into the database hotel_reviews

    :param df: Dataframe to be inserted
    :param table: Name of table where data is to be inserted
    :param if_exists: What to do if the table already exists. Option are replace: fail, replace & append(default)
    """
    print("Inserting data into database per 10000 rows")
    df.to_sql(name=table, con=engine, if_exists=if_exists, index=False, chunksize=10000)


def retrieve_table_into_df(table):
    """
    Retrieves all data from a specified table and returns a dataframa

    :param table: The table you want to retrieve data from
    :return: returns a dataframe of retrieved data from the table
    """
    df = pd.read_sql("SELECT * FROM "+table, con=engine)
    return df


def get_top_reviews(limit, label):
    """

    :param limit: Amount of reviews you want
    :param label: 0 for negative reviews, 1 for positive reviews
    :return:
    """
    query = "CALL SelectTopReviews({}, {});".format(limit, label)
    df = pd.read_sql_query(query, engine)

    return df
