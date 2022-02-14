
# The inital set of baby names and bith rates
names = ['Bob','Jessica','Mary','John','Mel']

births = [968, 155, 77, 578, 973]

BabyDataList = list(zip(names,births))
BabyDataList

import pandas as pd

df = pd.DataFrame(data = BabyDataList, columns=['Names', 'Births'])
df


## OR The shortcur , with the use of the workspace

df.to_csv("Hakim.csv", index=True,header=True)

fileName = ("Hakim.csv")
dfread2 = pd.read_csv(fileName)
dfread2


# Check data type of the columns
df.dtypes



# Check data type of Births column
df.Births.dtype

Sorted = df.sort_values(['Births'], ascending=False)
Sorted.head()


# Create graph
df['Births'].plot()

import plotly.express as px

fig = px.bar(df, x='Names', y='Births')
fig.show()

# Maximum value in the data set
MaxValue = df['Births'].max()

# Name associated with the maximum value
MaxName = df['Names'][df['Births'] == df['Births'].max()].values

# Text to display on graph
Text = str(MaxValue) + " - " + MaxName

# Add text to graph
plt.annotate(Text, xy=(1, MaxValue), xytext=(8, 0), 
                 xycoords=('axes fraction', 'data'), textcoords='offset points')

print("The most popular name")
df[df['Births'] == df['Births'].max()]
#Sorted.head(1) can also be used




