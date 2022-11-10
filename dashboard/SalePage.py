import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, Input, Output, html
from dash.exceptions import PreventUpdate

from figure import *

company_type = ["商品房", "住宅商品房", "别墅、高档公寓", "办公楼", "商业营业用房", "其他商品房"]

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

salePage = SalePage()

app.layout = dbc.Container([
    dbc.Container(
        dbc.Row([
            dbc.Col(dcc.Graph(id="ChineseMap", figure=salePage.getGeoMap()), width=6),
            dbc.Col(dcc.Graph(id="StackedChart", figure=salePage.getStackedChart()), width=6),
        ]),
        # style={"height": "30vh"},
    ),

    dbc.Container(
        dbc.Row([
            dbc.Col(dcc.Graph(id="Table", figure=salePage.getTable()), width=6),
            dbc.Col(dcc.Graph(id="ScatterChart", figure=salePage.getScatterChart()), width=6),
        ]),
        # style={"height": "30vh"},
    ),

])


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
