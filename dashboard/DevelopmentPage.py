import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from figure import *

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])
developmentPage = DevelopmentPage()

app.layout = dbc.Container([
    dbc.Card([
        dbc.CardHeader(html.H4("Number of Enterprises for Real Estate Development and Average Employed Persons")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(width=1),
                        dbc.Col("Current District: China", id="LineDistrict", width=8),
                        dbc.Col(dbc.Button("Reset", id="ResetButton", size="sm", style=dict(width=80)), width=3)
                    ]),
                    dbc.Row(dcc.Graph(id="LineChart", figure=developmentPage.getLineChart())),
                ], width=6),
                dbc.Col([
                    dbc.Row(
                        dbc.Checklist(
                            id="TypeChecklist",
                            options=[{"label": company_type[e], "value": e} for e in company_type],
                            inline=True
                        ),
                    ),
                    dbc.Row([
                        dbc.Col(width=9),
                        dbc.Col(dbc.Switch(id='DescendingSwitch', value=True, label="Descending"), width=3)
                    ]),
                    dbc.Row(dcc.Graph(id="BarChart", figure=developmentPage.getBarChart())),
                ], width=6),
            ]),
        ]),
    ]),
    html.Br(),
    dbc.Card([
        dbc.CardHeader(
            dbc.Row([
                dbc.Col([
                    html.H4(
                        "Assets and Liabilities of Enterprises for Real Estate Development"),
                ], width=8),
                dbc.Col(
                    dcc.Dropdown(id="StackedDistrict",
                                 options=[{"label": to_pinyin[convertProvince(e)], "value": convertProvince(e)}
                                          for e in list(set(data["地区"]))],
                                 value="全国", clearable=False),
                    width={"size": 3, "offset": 1}
                )
            ])
        ),
        dbc.CardBody(dcc.Graph(id="StackedChart", figure=developmentPage.getStackedChart())),
        dbc.CardFooter(html.Div("Total Assets = Owner's Equity + Total Liabilities; "
                                "Assets Liabilities Rate = (Total Liabilities) / (Total Assets)",
                                style=dict(fontSize=5)
                                ))
    ]),
    html.Br(),
    dbc.Card([
        dbc.CardHeader(html.H4("Income and Revenue of Enterprises for Real Estate Development")),
        dbc.CardBody(dcc.Graph(id="BubbleChart", figure=developmentPage.getBubbleChart())),
        dbc.CardFooter(html.Div("In the bubble chart, the size of bubble indicates the total income;"
                                "Revenue Rate = (Total Revenue) / (Total Income)",
                                style=dict(fontSize=5)
                                ))
    ]),

])

button_click_cache = [0, []]


@app.callback(
    [Output("LineDistrict", "children"),
     Output("LineChart", "figure")],
    [Input("BarChart", "clickData"),
     Input("TypeChecklist", "value"),
     Input("ResetButton", "n_clicks")]
)
def updateLineChart(click_data, names, n_clicks):
    if click_data and n_clicks == button_click_cache[0] and names == button_click_cache[-1]:
        district = click_data["points"][0]["y"]
    else:
        button_click_cache[0] = n_clicks
        button_click_cache[-1] = names
        district = "China"
    return ["Current District: " + district,
            developmentPage.getLineChart(district=from_pinyin[district], names=button_click_cache[-1])]


@app.callback(

    Output("StackedChart", "figure"),
    Input("StackedDistrict", "value")
)
def updateStackedChart(district):
    return developmentPage.getStackedChart(district=district)


@app.callback(
    Output("BarChart", "figure"),
    [
        Input("LineChart", "hoverData"),
        Input("TypeChecklist", "value"),
        Input("DescendingSwitch", "value")
    ],
)
def updateBarChart(hover_Data, building_types, descending):
    if not hover_Data:
        return developmentPage.getBarChart(building_types=building_types, descending=descending)

    point = hover_Data["points"][0]
    year = point["x"]
    name = "房地产开发企业平均从业人数(人)" if point["curveNumber"] else "房地产开发企业个数(个)"

    return developmentPage.getBarChart(name=name, year=year,
                                       building_types=building_types,
                                       descending=descending)


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
