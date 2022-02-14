import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

dname = os.getcwd()
os.chdir(dname)
full_path = os.path.realpath('chickweight.csv')
dfChickens = pd.read_csv(full_path)

# 1. select columns
chickensDiet = dfChickens[['weight', 'diet']]
# 2. select rows
chickenOnDiet = dfChickens.loc[dfChickens['diet'] == 4]
# 3. rename columns
reNameChicks = dfChickens.rename(columns={'chick' : 'chickNumber', 'diet' :
    'food'})
# 4. sort rows
sortChickWeight = dfChickens.sort_values(by='weight', ascending=False)
# 5. add new column with new data(adding data used to be step 6
dfChickens['beeksize'] = np.random.randint(1, 20, dfChickens.shape[0])
# 7. summarize statistics
dfWeightFood = dfChickens.groupby("diet").mean().reset_index()
# 8. create plot/bar/.....
plotWeight = px.bar(dfWeightFood, x='diet', y='weight')
plotWeight.show()