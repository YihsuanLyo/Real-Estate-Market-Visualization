import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output
from dash.exceptions import PreventUpdate

from figure import *

building_type = ["内资", "国有", "集体", "港、澳、台投资", "外商投资"]

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])
developmentPage = DevelopmentPage()

app.layout = dbc.Container([
    dbc.Card([
        dbc.CardHeader("个数及平均从业人数"),
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col([
                        # dcc.Checklist(
                        dbc.Row(
                            dbc.Checklist(
                                id="TypeChecklist",
                                options=[{"label": e, "value": e} for e in building_type],
                                inline=True
                            ),
                        ),
                        dcc.Graph(id="LineChart", figure=developmentPage.getLineChart()),
                    ], width=5),
                    dbc.Col([
                        dbc.Row(
                            dbc.Switch(id='DescendingSwitch', value=True, label="Descending"),
                        ),
                        dbc.Row(dcc.Graph(id="BarChart", figure=developmentPage.getBarChart())),
                    ], width=5),
                    dbc.Col(dcc.Graph(id="PieChart", figure=developmentPage.getPieChart()), width=2),
                ]
            )
        ),

    ]),

    dbc.Card([
        dbc.CardHeader("StackedChart"),
        dbc.CardBody(dcc.Graph(id="StackedChart", figure=developmentPage.getStackedChart())),
    ]),
    dbc.Card([
        dbc.CardHeader("BubbleChart"),
        dbc.CardBody(dcc.Graph(id="BubbleChart", figure=developmentPage.getBubbleChart())),
    ]),

    # dbc.Row([
    #     dbc.Col
    #     dbc.Col(dcc.Graph(id="BubbleChart", figure=developmentPage.getBubbleChart()), width=6),
    # ]),

    dbc.Row([
    ]),
])


@app.callback(
    Output("BarChart", "figure"),
    [
        Input("LineChart", "hoverData"),
        Input("TypeChecklist", "value"),
        Input("DescendingSwitch", "value")
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
    district = hover_data["points"][0]["y"]
    for e in allDistricts():
        if e.startswith(district):
            district = e
            break
    return developmentPage.getStackedChart(district=district)


@app.callback(
    Output("LineChart", "figure"),
    [Input("BarChart", "hoverData"),
     Input("TypeChecklist", "value")]
)
def updateLineChart(hover_data, names):
    district = hover_data["points"][0]["y"] if hover_data else "全国"
    return developmentPage.getLineChart(district=district, names=names)


pie_cache = ["全国", 2020, "房地产开发企业个数(个)"]
@app.callback(
    Output("PieChart", "figure"),
    [Input("BarChart", "hoverData"),
     Input("LineChart", "hoverData")]
)
def updatePieChart(bar_hover, line_hover):
    if bar_hover:
        pie_cache[0] = bar_hover["points"][0]["y"]
    if line_hover:
        pie_cache[1] = line_hover["points"][0]["x"]
        pie_cache[2] = "房地产开发企业平均从业人数(人)" if line_hover["points"][0]["curveNumber"] else "房地产开发企业个数(个)"

    return developmentPage.getPieChart(*pie_cache)


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
