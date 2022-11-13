import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output

from figure import *

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

salePage = SalePage()
building_types = salePage.keys["商品房"]

app.layout = dbc.Container([
    dbc.Row(
        dbc.Card([
            dbc.CardHeader("销售额与销售面积"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            options=["销售面积(万平方米)", "销售额(亿元)"],
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
                            options=building_types,
                            placeholder="商品房",
                            id="BuildingTypes",
                            multi=True
                        ),
                        width=6
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
                dbc.CardHeader("平均销售价格"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(
                            dcc.Dropdown(
                                options=allDistricts(),
                                placeholder="全国",
                                id="SelectedDistricts",
                                multi=True
                            ), width=8
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                options=["商品房"] + salePage.keys["商品房"],
                                value="商品房",
                                id="AverageBuildingType",
                                clearable=False
                            ), width=4
                        )
                    ]),
                    dbc.Row(
                        dcc.Graph(id="AveragePriceChart", figure=salePage.getAveragePriceTable())
                    ),
                ])
            ]),
            width=6
        ),
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("2010-2020各省份房屋竣工套数与销售套数关系"),
                dbc.CardBody(
                    dbc.Row(
                        dcc.Graph(id="ScatterChart", figure=salePage.getScatterChart())
                    ),
                )
            ]),
            width=6
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
    # year = hover_data["points"][0]["x"] if hover_data else 2020
    return salePage.getGeoMap(name=name, building_types=types, year=year)


@app.callback(
    Output("StackedChart", "figure"),
    [Input("BuildingTypes", "value"),
     Input("DataType", "value"),
     Input("ChineseMap", "hoverData")]
)
def updateMap(types, name, hover_data):
    district = hover_data["points"][0]["location"] if hover_data else "全国"
    return salePage.getStackedChart(name=name, building_types=types, district=district)


@app.callback(
    Output("AveragePriceChart", "figure"),
    [Input("SelectedDistricts", "value"),
     Input("AverageBuildingType", "value")]
)
def updateTable(districts, building_type):
    return salePage.getAveragePriceBar(districts=districts, building_type=building_type)


if __name__ == '__main__':
    app.run_server(debug=True, port=8081)