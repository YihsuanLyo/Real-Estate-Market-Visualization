import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output

from figure import *

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

investmentPage = InvestmentPage()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Graph(id="InvestmentLine", figure=investmentPage.getInvestmentPlanChart()), width=4),
        dbc.Col(dcc.Graph(id="Treemap", figure=investmentPage.getInvestmentTreemap()), width=4),
        dbc.Col(dcc.Graph(id="ConstructionLine", figure=investmentPage.getConstructingAreaChart()), width=4),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="InvestmentTable", figure=investmentPage.getInvestmentTable()), width=8),
        dbc.Col(dcc.Graph(id="PieChart", figure=investmentPage.getNewConstructionPie()), width=4),
    ]),
])


@app.callback(
    Output("Treemap", "figure"),
    Input("InvestmentLine", "hoverData")
)
def update_treemap(hover_data):
    year = hover_data["points"][0]["x"] if hover_data else 2020
    return investmentPage.getInvestmentTreemap(year=year)


@app.callback(
    Output("InvestmentTable", "figure"),
    Input("InvestmentLine", "hoverData")
)
def update_treemap(hover_data):
    year = hover_data["points"][0]["x"] if hover_data else 2020
    return investmentPage.getInvestmentTable(year=year)


if __name__ == '__main__':
    app.run_server(debug=True, port=8082)
