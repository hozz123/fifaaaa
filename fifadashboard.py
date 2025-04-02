#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


url = "https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"
tables = pd.read_html(url)
df = tables[3]  

# rename
df = df.rename(columns={
    'Year': 'Year',
    'Winners': 'Winner',
    'Runners-up': 'RunnerUp'
})

# west Germany and Germany
df['Winner'] = df['Winner'].replace({'West Germany': 'Germany'})
df['RunnerUp'] = df['RunnerUp'].replace({'West Germany': 'Germany'})


win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# dropdown lists
winning_countries = df['Winner'].dropna().unique()
all_years = df['Year'].dropna().unique()

# dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),

    html.H3("World Cup Wins by Country"),
    dcc.Graph(id='choropleth'),

    html.Label("Select a Country:", style={'fontWeight': 'bold'}),
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in sorted([c for c in winning_countries if isinstance(c, str)])],
        placeholder="Select a country"
    ),
    html.Div(id="country-output", style={'marginBottom': '30px'}),

    html.Label("Select a Year:", style={'fontWeight': 'bold'}),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": y, "value": y} for y in sorted([y for y in all_years if not pd.isna(y)])],
        placeholder="Select a year"
    ),
    html.Div(id="year-output")
])



# choropleth map
@app.callback(
    Output("choropleth", "figure"),
    Input("country-dropdown", "value")
)
def update_choropleth(_):
    fig = px.choropleth(
        win_counts,
        locations="Country",
        locationmode="country names",
        color="Wins",
        title="FIFA World Cup Wins",
        color_continuous_scale=px.colors.sequential.Plasma,
        projection="natural earth"
    )
    return fig

# country win output
@app.callback(
    Output("country-output", "children"),
    Input("country-dropdown", "value")
)
def show_country_wins(country):
    if country:
        wins = win_counts[win_counts['Country'] == country]['Wins'].values[0]
        return f"{country} has won the FIFA World Cup {wins} times."
    return "Select a country to view win count."

# year result
@app.callback(
    Output("year-output", "children"),
    Input("year-dropdown", "value")
)
def show_year_results(year):
    if year:
        row = df[df['Year'] == year]
        if not row.empty:
            winner = row['Winner'].values[0]
            runner = row['RunnerUp'].values[0]
            return f"In {year}, the winner was {winner} and the runner-up was {runner}."
    return "Select a year to view the result."


import os

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))












