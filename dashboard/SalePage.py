import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html

from figure import *

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

salePage = SalePage()
building_types = salePage.keys["商品房"]

app.layout = dbc.Container([
    dbc.Row(
        dbc.Card([
            dbc.CardHeader(html.H4("Total Sale and Floor Space of Commercialized Buildings")),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            options=[{"label": html.Div("Floor Space of Building Sold (10000 sq.m)",
                                                        style={"font-size": 14}),
                                      "value": "销售面积(万平方米)", },
                                     {"label": html.Div("Total Sale (100 million yuan)",
                                                        style={"font-size": 14}),
                                      "value": "销售额(亿元)"}],
                            value="销售额(亿元)",
                            id="DataType",
                            clearable=False,
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dcc.Slider(
                            id="YearSlider",
                            min=2010,
                            max=2020,
                            step=1,
                            value=2010,
                            marks=dict(zip(list(range(2010, 2021, 2)),
                                           [str(e) for e in range(2010, 2021, 2)])),
                            included=False
                        ),
                        width=3
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            options=[{"label": building_types[e], "value": e}
                                     for e in building_types if e != "商品房"],
                            placeholder="Commercialized Buildings",
                            id="BuildingTypes",
                            multi=True
                        ),
                        width=5
                    ),
                    dbc.Col(
                        dbc.Button("Reset", id="ResetButton"),
                        width=1
                    )

                ]),
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id="ChineseMap", figure=salePage.getGeoMap()),
                        width=6
                    ),
                    dbc.Col(
                        dcc.Graph(id="StackedChart", figure=salePage.getStackedChart()),
                        width=6
                    )
                ])
            ])
        ])
    ),
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Comparison of Average Selling Price of Commercialized Buildings (yuan/sq.m)"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                options=[{"label": to_pinyin[convertProvince(e)], "value": e}
                                         for e in allDistricts()],
                                placeholder="China",
                                id="SelectedDistricts",
                                multi=True
                            ), width=7
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                options=[{"label": html.Div(salePage.keys["商品房"][e],
                                                            style={"font-size": 15 if "住宅" not in e else 13}),
                                          "value": e}
                                         for e in salePage.keys["商品房"]],
                                value="商品房",
                                id="AverageBuildingType",
                                clearable=False
                            ), width=5
                        )
                    ]),
                    dbc.Row(
                        dcc.Graph(id="AveragePriceChart", figure=salePage.getAveragePriceBar())
                    ),
                ])
            ]),
            width=7
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.Div("Relationship between the Number of Completed Flats and "
                                        "Sold Flats of Residential Buildings", style={"font-size": 16})),
                dbc.CardBody(
                    dbc.Row(
                        dcc.Graph(id="ScatterChart", figure=salePage.getScatterChart())
                    ),
                ),
                dbc.CardFooter(dcc.Markdown("In the scatter chart, Line *y=x* is used to separate the scatters, "
                                            "with upper scatters indicating *Completed > Sold* "
                                            "and lower scatters indicating *Completed < Sold*",
                                            style=dict(fontSize=10)))
            ]),
            width=5
        )
    ]),

])


@app.callback(
    Output("ChineseMap", "figure"),
    [Input("BuildingTypes", "value"),
     Input("DataType", "value"),
     # Input("StackedChart", "hoverData"),
     Input("YearSlider", "value")]
)
def updateMap(types, name, year):
    return salePage.getGeoMap(name=name, building_types=types, year=year)


button_click_cache = [0]
@app.callback(
    Output("StackedChart", "figure"),
    [Input("BuildingTypes", "value"),
     Input("DataType", "value"),
     Input("ChineseMap", "hoverData"),
     Input("ResetButton", "n_clicks")]
)
def updateStackedChart(types, name, hover_data, n_clicks):
    if n_clicks != button_click_cache[0] or not hover_data:
        district = "China"
        button_click_cache[0] = n_clicks
    else:
        district = hover_data["points"][0]["location"]
    return salePage.getStackedChart(name=name, building_types=types, district=district)


@app.callback(
    Output("AveragePriceChart", "figure"),
    [Input("SelectedDistricts", "value"),
     Input("AverageBuildingType", "value")]
)
def updateBarChart(districts, building_type):
    return salePage.getAveragePriceBar(districts=districts, building_type=building_type)


if __name__ == '__main__':
    app.run_server(debug=True, port=8081)
