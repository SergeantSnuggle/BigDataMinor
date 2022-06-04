## https://plot.ly/python/


import pandas as pd
import plotly.graph_objects as go

# First plotly
fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
    layout_title_text="A Figure Displayed with fig.show()"
)
fig.show()

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

df.head()

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

## for Plotly x- axis values need to be sorted first ;-(
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
