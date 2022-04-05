import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import plotly.io as pio
pio.renderers.default = "browser"


def show_result_plot(dfResults, title=""):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    dfResults = dfResults.sort_values(by='rank_test_score').reset_index(drop=True)
    x = dfResults['rank_test_score'].head(10)
    y = dfResults['mean_fit_time'].head(10)
    y2 = dfResults['mean_test_score'].head(10) * 100
    fig.add_trace(go.Scatter(x=x, y=y, name="Time", text=x, mode="lines+markers+text", textposition="top center"),
                  secondary_y=False, )
    fig.add_trace(go.Scatter(x=x, y=y2, name="Score", mode="lines+markers"),
                  secondary_y=True, )
    fig.update_xaxes(title_text="Results from " + title)
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Time</b> (in seconden)", secondary_y=False)
    fig.update_yaxes(title_text="<b>Score</b> (in procenten)", secondary_y=True)
    fig.show()


df = pd.read_csv("LrTfIdfresults.csv")
show_result_plot(df, "Logistic Regression Countvectorizer")