## https://plot.ly/python/


import plotly.express as px


## Now Plotly EXPRESS
## with px comes gapminder data

data_canada = px.data.gapminder().query("country == 'Canada'")

fig = px.bar(data_canada, x='year', y='pop')
fig.show()

data_canada.head()

## Some more bar plot in PlotLy Express


fig = px.bar(data_canada, x='year', y='pop',
             hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
             labels={'pop':'population of Canada'}, height=400)
fig.show()

## line plot PlotLy Express

gapminder = px.data.gapminder().query("continent == 'Oceania'")
fig = px.line(gapminder, x='year', y='lifeExp', color='country')
fig.show()

##

tips = px.data.tips()
fig = px.bar(tips, x="total_bill", y="sex", color='day', orientation='h',
             hover_data=["tip", "size"],
             height=400,
             title='Restaurant bills')
fig.show()

import pandas as pd
df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

df.head()

# scatter plot in PLotly Express

fig=px.scatter(df,x="gdp per capita",y="life expectancy",
                height=400)

fig.show()

fig=px.scatter(df,x="gdp per capita",y="life expectancy",
                height=400)
fig.update_xaxes(type="log")           
fig.show()


## Back to Plotly, ugly scatterplot

fig = go.Figure(data=[
    go.Scatter(
        x=df["gdp per capita"],
        y=df["life expectancy"],
        #mode='markers',
    )
])
fig.update_xaxes(type="log")
fig.show()

## for plotly x- axis values need to be sorted first ;-(
dfsorted = df.sort_values("gdp per capita")

fig = go.Figure(data=[
    go.Scatter(
        x=dfsorted["gdp per capita"],
        y=dfsorted["life expectancy"],
        mode='markers',
    )
])
fig.update_xaxes(type="log")


fig.show()
