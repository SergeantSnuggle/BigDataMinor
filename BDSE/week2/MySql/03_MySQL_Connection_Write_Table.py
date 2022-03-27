# https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html

# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/


import pandas as pd

from sqlalchemy import create_engine, inspect


df=pd.read_csv('population.csv', sep=',')

df.head()


# create db first in MySQL
engine = create_engine('mysql://root@localhost:3306/zipcode')
df.to_sql(name='newpopulation',con=engine,if_exists='replace',index=False, chunksize=1000)

df1 = pd.read_sql("SELECT * FROM newpopulation", con=engine)
df1.head()






