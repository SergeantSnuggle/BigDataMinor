import pandas as pd
# more ugly df= pd.read_csv('IMDb movies.csv')
dfIMDB = pd.read_csv('week2\\IMDb movies.csv', sep=',')


dfTitleBudget = dfIMDB[['title', 'budget']]
#1a Only dollar
dfDollar = dfTitleBudget[dfTitleBudget['budget'].str.contains("$", na=False, regex=False)]

#1b remove dollar
dfBudget = dfDollar['budget'].str.strip('$').to_frame()

#1c change to numerical
dfBudget['budget'] = dfBudget.budget.astype(float)

#2 split genre into collumns
dfGenreSplit = dfIMDB.genre.str.split(pat=',', expand=True)

#3a Add a column ‘numberOfActors’ containing the number of actors mentioned in the column ‘actors`

#3b Add a column ‘mainActor’ containing only the first mentioned actor in the column ‘actors