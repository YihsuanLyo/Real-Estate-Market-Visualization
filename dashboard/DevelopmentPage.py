

import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, Input, Output, html
from dash.exceptions import PreventUpdate

from figure import *

building_type = ["内资", "国有", "集体", "港、澳、台投资", "外商投资"]

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])
developmentPage = DevelopmentPage()

app.layout = dbc.Container([
    dbc.Container(
        dbc.Row([
            dbc.Col(dcc.Graph(id="LineChart", figure=developmentPage.getLineChart()), width=6),
            dbc.Col(dcc.Graph(id="BubbleChart", figure=developmentPage.getBubbleChart()), width=6),
        ]),
        # style={"height": "30vh"},
    ),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    dcc.Checklist(
                        id="TypeChecklist",
                        options=[{"label": e, "value": e} for e in building_type],
                        inline=True
                    ),
                    width=8
                ),
                dbc.Col(
                    html.P("Descending:"),
                    width=2,
                ),
                dbc.Col(
                    daq.BooleanSwitch(id='Descending', on=True),
                    width=2,
                )
            ],
                className="g-0",
            ),
            dbc.Row(dcc.Graph(id="BarChart", figure=developmentPage.getBarChart())),
        ],
            width=6),
        dbc.Col(dcc.Graph(id="StackedChart", figure=developmentPage.getStackedChart()), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="PieChart", figure=developmentPage.getPieChart()), width=3),
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
