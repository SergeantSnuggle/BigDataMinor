import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqlconnector://root:admin@localhost/zipcode')

# FIRST EMBEDDED RAW SQL

df = pd.read_sql("SELECT * FROM population", con=engine)

df.head()

# NEXT MORE UGLY EMBEDDED RAW SQL

df1 = pd.read_sql("SELECT * FROM population where state='MA'", con=engine)


# TRY TO PARAMETRIZE THE QUERY WITH STRING GLUEING

state="TX"
query="SELECT * FROM population WHERE State='"+ state+ "'"

df2 = pd.read_sql(query, con=engine)

# LAST, FOR STORED PROCEDURES WE NEED SOMETHING ELSE, A RAW CONNECTION
# UNFORTUNATELY THE RESPONSE NEEDS SOME WORK


from contextlib import closing

conn = engine.raw_connection()
cur=conn.cursor()
cur.callproc('SelectByState', ['CA'])
for row in cur.stored_results(): 
    results = row.fetchall()
    colNamesList=row.description

df3 = pd.DataFrame(results)

colNames=[i[0] for i in colNamesList]

result_dicts = [dict(zip(colNames, row)) for row in results]

df4=pd.DataFrame(result_dicts)

conn.close()

# THIRD,  CLEANER WITH THE USE OF A FUNCTION

# Call procedure
def call_stored_procedure(sql_engine,function_name, params):
    connection = sql_engine.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc(function_name, params)
        for row in cursor.stored_results(): 
            results = row.fetchall()
            colNamesList=row.description
 
        colNames=[i[0] for i in colNamesList]
        result_dicts = [dict(zip(colNames, row)) for row in results]
        result_df=pd.DataFrame(result_dicts)
        cursor.close()
        #connection.commit()
        return result_df
    finally:
        connection.close()

function_name="SelectByState"
state='CA'
params =[state]


df5 = call_stored_procedure(engine,function_name,params )

