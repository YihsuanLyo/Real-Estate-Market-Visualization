import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, Input, Output, html
from dash.exceptions import PreventUpdate

from figure import *

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

investmentPage = InvestmentPage()

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(dcc.Graph(id="InvestmentLine", figure=investmentPage.getInvestmentPlanChart())),
        dbc.Col(dcc.Graph(id="Treemap", figure=investmentPage.getInvestmentTreemap())),
        dbc.Col(dcc.Graph(id="InvestmentTable", figure=investmentPage.getInvestmentTable())),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id="ConstructionLine", figure=investmentPage.getConstructingAreaChart())),
        dbc.Col(dcc.Graph(id="PieChart", figure=investmentPage.getNewConstructionPie())),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
