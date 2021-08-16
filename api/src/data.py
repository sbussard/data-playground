import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd
import pandasql as ps
from plotly.utils import PlotlyJSONEncoder

# precompute to waste memory / save time
source = pd.read_csv(
    'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv', delimiter=',')
data = None


def munge():
    global data
    if data is None:
        data = ps.sqldf("""
            SELECT
            date,
            100 * total_deaths / total_cases AS mortality_rate,
            100 * new_deaths / new_cases AS ephemeral_mortality_rate,
            100 * LEAD(total_deaths, 56) OVER (ORDER BY date ASC) / total_cases AS adjusted_mortality_rate,
            100 * LEAD(new_deaths, 56) OVER (ORDER BY date ASC) / new_cases AS adjusted_ephemeral_mortality_rate
            FROM source WHERE iso_code = 'USA'
            ORDER BY date ASC
        """)

    # Data Collected from https://github.com/owid/covid-19-data/tree/master/public/data on 2021/02/18
    # return json.loads(data.to_json(orient='records'))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.get('date'), y=data.get(
        'ephemeral_mortality_rate'), mode='lines', name='Ephemeral Case Fatality Rate (Percent)'))
    fig.add_trace(go.Scatter(x=data.get('date'), y=data.get(
        'mortality_rate'), mode='lines', name='Case Fatality Rate (Percent)'))
    fig.add_trace(go.Scatter(x=data.get('date'), y=data.get(
        'adjusted_mortality_rate'), mode='lines', name='Adjusted Case Fatality Rate (Percent)'))
    fig.add_trace(go.Scatter(x=data.get('date'), y=data.get('adjusted_ephemeral_mortality_rate'),
                             mode='lines', name='Adjusted Ephemeral Case Fatality Rate (Percent)'))
    fig.update_layout(annotations=[
        {
            "xref": "paper",
            "yref": "paper",
            "x": 0.0,
            "y": 1.05,
            "xanchor": "left",
            "yanchor": "bottom",
            "text": "Covid Case Fatality Rate",
            "font": {"family": "Arial", "size": 30, "color": "rgb(37,37,37)"},
            "showarrow": False,
        },
        {
            "xref": "paper",
            "yref": "paper",
            "x": 0.5,
            "y": -0.1,
            "xanchor": "center",
            "yanchor": "top",
            "text": "Source: Our World in Data",
            "font": {"family": "Arial", "size": 12, "color": "rgb(150,150,150)"},
            "showarrow": False,
        },
    ])
    fig.update_layout(yaxis=dict(range=[-5, 20]))

    return json.dumps(fig, cls=PlotlyJSONEncoder)
