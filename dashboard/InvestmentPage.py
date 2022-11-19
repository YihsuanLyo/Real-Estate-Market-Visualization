import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
from dash.exceptions import PreventUpdate

from figure import *

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

investmentPage = InvestmentPage()

app.layout = dbc.Container([
    dbc.Card([
        dbc.CardHeader([
            dbc.Row([
                dbc.Col([
                    html.H3("Investment"),
                ], width=3),
                dbc.Col(
                    dcc.Dropdown(id="InvestmentDistrict",
                                 options=[{"label": to_pinyin[convertProvince(e)], "value": convertProvince(e)}
                                          for e in list(set(data["地区"]))],
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
        ]),
        dbc.CardFooter(dcc.Markdown("Notice: Completed Investment is **not consisted of** but can be"
                                    " **classified by** Size of Projects, Type of Buildings and Usage of Funds",
                                    style=dict(fontSize=10)))
    ]),
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
    keys = investmentPage.keys["分类"]
    if sunburst_click:
        name = sunburst_click["points"][0]["label"]
        for key in keys:
            if keys[key] == name:
                name = key
                break
    else:
        name = "项目规模"
    if name not in investmentPage.keys:
        raise PreventUpdate
    year = line_hover["points"][0]["x"] if line_hover else 2020
    return investmentPage.getInvestmentTable(year=year, name=name, district=district)


if __name__ == '__main__':
    app.run_server(debug=True, port=8082)
