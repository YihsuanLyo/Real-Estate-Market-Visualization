import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
from dash.exceptions import PreventUpdate

from figure import *

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

investmentPage = InvestmentPage()

app.layout = dbc.Container([
    dbc.Row(
        dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        html.H3("资金情况"),
                    ], width=3),
                    dbc.Col(
                        dcc.Dropdown(id="InvestmentDistrict", options=list(set(data["地区"])),
                                     value="全国", clearable=False),
                        width={"size": 3, "offset": 6}
                    )
                ])
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        dcc.Graph(id="InvestmentLine", figure=investmentPage.getInvestmentPlanChart()),
                        width=8
                    ),
                    dbc.Col(
                        dcc.Graph(id="InvestmentSunburst", figure=investmentPage.getInvestmentSunburst()),
                        width=4
                    ),
                ]
                ),
                dbc.Row(
                    dcc.Graph(id="InvestmentTable", figure=investmentPage.getInvestmentTable())
                ),
            ])
        ])
    ),

    dbc.Row(
        dbc.Card([
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col([
                        html.H3("施工情况"),
                    ], width=3),
                    dbc.Col(
                        dcc.Dropdown(id="ConstructionDistrict", options=list(set(data["地区"])),
                                     value="全国", clearable=False),
                        width={"size": 3, "offset": 6}
                    )
                ])
            ),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col([
                        dbc.Row(
                            dcc.Graph(id="ConstructionLine", figure=investmentPage.getConstructingAreaChart())
                        ),
                        dbc.Row(
                            dcc.Graph(id="ValueLine", figure=investmentPage.getConstructingValueChart())
                        )
                    ], width=8),
                    dbc.Col(
                        dcc.Graph(id="ConstructionTreemap", figure=investmentPage.getConstructionTreemap()),
                        width=4
                    )
                ])
            )
        ]),
    ),

])


@app.callback(
    Output("InvestmentLine", "figure"),
    Input("InvestmentDistrict", "value")
)
def update_investment_line(district):
    return investmentPage.getInvestmentPlanChart(district=district)


@app.callback(
    Output("InvestmentSunburst", "figure"),
    [Input("InvestmentLine", "hoverData"),
     Input("InvestmentDistrict", "value")]
)
def update_sunburst(hover_data, district):
    year = hover_data["points"][0]["x"] if hover_data else 2020
    return investmentPage.getInvestmentSunburst(year=year, district=district)


@app.callback(
    Output("InvestmentTable", "figure"),
    [Input("InvestmentLine", "hoverData"),
     Input("InvestmentSunburst", "clickData"),
     Input("InvestmentDistrict", "value")]
)
def update_table(line_hover, sunburst_click, district):
    name = sunburst_click["points"][0]["label"][1:5] if sunburst_click else "项目规模"
    if name not in investmentPage.keys:
        raise PreventUpdate
    year = line_hover["points"][0]["x"] if line_hover else 2020
    return investmentPage.getInvestmentTable(year=year, name=name, district=district)

@app.callback(
    Output("ConstructionLine", "figure"),
    Input("ConstructionDistrict", "value")
)
def update_area_line(district):
    return investmentPage.getConstructingAreaChart(district=district)

@app.callback(
    Output("ValueLine", "figure"),
    Input("ConstructionDistrict", "value")
)
def update_value_line(district):
    return investmentPage.getConstructingValueChart(district=district)


@app.callback(
    Output("ConstructionTreemap", "figure"),
    [Input("ConstructionLine", "hoverData"),
     Input("ConstructionDistrict", "value")]
)
def update_treemap(line_hover, district):
    year = line_hover["points"][0]["x"] if line_hover else 2020
    return investmentPage.getConstructionTreemap(year=year, district=district)


if __name__ == '__main__':
    app.run_server(debug=True, port=8082)
