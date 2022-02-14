import pandas as pd
import plotly.express as px

dfimdb = pd.read_csv('IMDb movies.csv')
dfimdb

#Nr1. Number of rows
print("Number of rows: \t", dfimdb.shape[0])

#Nr2. Number of cols
print("Number of cols: \t", dfimdb.shape[1])

#Nr3. Mean of film duration
dfimdbMean = dfimdb['duration'].mean()
print("Mean durration: \t", round(dfimdbMean, 2))

#Nr4. How many USA movies
dfimdbUsa = dfimdb['country'].value_counts()['USA']
print("Number of USA movies: \t", dfimdbUsa)

#Nr5. Longest Title
field_length = dfimdb.title.astype(str).map(len)
print(dfimdb.loc[field_length.argmax(), "title"])

#Nr6. Plot
dfimdbMoviesYear = dfimdb.groupby('year').count().reset_index()
fig = px.bar(dfimdbMoviesYear, x='year', y='title')
fig.show()
