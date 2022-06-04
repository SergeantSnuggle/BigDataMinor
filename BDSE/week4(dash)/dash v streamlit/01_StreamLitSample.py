import streamlit as st
import json
import plotly.graph_objects as go

with open("fig.json", "r") as f:
    fig = go.Figure(json.load(f))
st.write(fig)