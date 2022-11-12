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
    dbc.Row([
        dbc.Col([
            dcc.Checklist(
                id="TypeChecklist",
                options=[{"label": e, "value": e} for e in building_type],
                inline=True
            ),
            dcc.Graph(id="LineChart", figure=developmentPage.getLineChart()),
        ], width=6),
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    html.P("Descending:"),
                    width=2,
                ),
                dbc.Col(
                    daq.BooleanSwitch(id='DescendingSwitch', on=True),
                    width=2,
                ),
                dbc.Row(dcc.Graph(id="BarChart", figure=developmentPage.getBarChart())),
            ]),
        ], width=6),
    ]),
    # style={"height": "30vh"},

    dbc.Row([
        dbc.Col(dcc.Graph(id="StackedChart", figure=developmentPage.getStackedChart()), width=6),
        dbc.Col(dcc.Graph(id="BubbleChart", figure=developmentPage.getBubbleChart()), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id="PieChart", figure=developmentPage.getPieChart()), width=3),
    ]),
])


@app.callback(
    Output("BarChart", "figure"),
    [
        Input("LineChart", "hoverData"),
        Input("TypeChecklist", "value"),
        Input("DescendingSwitch", "on")
    ],
)
def update_bar_chart(hover_Data, building_types, descending):
    if not hover_Data:
        return developmentPage.getBarChart(building_types=building_types, descending=descending)

    point = hover_Data["points"][0]
    year = point["x"]
    name = "房地产开发企业平均从业人数(人)" if point["curveNumber"] else "房地产开发企业个数(个)"

    return developmentPage.getBarChart(name=name, year=year,
                                       building_types=building_types,
                                       descending=descending)


@app.callback(
    Output("StackedChart", "figure"),
    Input("BarChart", "hoverData")
)
def updateStackedChart(hover_data):
    if not hover_data:
        raise PreventUpdate
    point = hover_data["points"][0]
    district = point["y"]
    return developmentPage.getStackedChart(district=district)


@app.callback(
    Output("LineChart", "figure"),
    [Input("BarChart", "hoverData"),
     Input("TypeChecklist", "value")]
)
def updateStackedChart(hover_data, names):
    district = hover_data["points"][0]["y"] if hover_data else "全国"
    return developmentPage.getLineChart(district=district, names=names)


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
