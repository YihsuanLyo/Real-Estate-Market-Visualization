import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html

from figure import *

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

constructionPage = ConstructionPage()

app.layout = dbc.Container([
    dbc.Card([
        dbc.CardHeader(
            dbc.Row([
                dbc.Col([
                    html.H3("Construction"),
                ], width=3),
                dbc.Col(
                    dcc.Dropdown(id="ConstructionDistrict",
                                 options=[{"label": to_pinyin[convertProvince(e)], "value": convertProvince(e)}
                                          for e in list(set(data["地区"]))],
                                 value="全国", clearable=False),
                    width={"size": 3, "offset": 6}
                )
            ])
        ),
        dbc.CardBody(
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        dcc.Graph(id="ConstructionLine", figure=constructionPage.getConstructingAreaChart())
                    ),
                    dbc.Row(
                        dcc.Graph(id="ValueLine", figure=constructionPage.getConstructingValueChart())
                    )
                ], width=8),
                dbc.Col(
                    dcc.Graph(id="ConstructionTreemap", figure=constructionPage.getConstructionTreemap()),
                    width=4
                )
            ])
        )
    ]),
])


@app.callback(
    Output("ConstructionLine", "figure"),
    Input("ConstructionDistrict", "value")
)
def update_area_line(district):
    return constructionPage.getConstructingAreaChart(district=district)


@app.callback(
    Output("ValueLine", "figure"),
    Input("ConstructionDistrict", "value")
)
def update_value_line(district):
    return constructionPage.getConstructingValueChart(district=district)


@app.callback(
    Output("ConstructionTreemap", "figure"),
    [Input("ConstructionLine", "hoverData"),
     Input("ConstructionDistrict", "value")]
)
def update_treemap(line_hover, district):
    year = line_hover["points"][0]["x"] if line_hover else 2020
    return constructionPage.getConstructionTreemap(year=year, district=district)


if __name__ == '__main__':
    app.run_server(debug=True, port=8083)
