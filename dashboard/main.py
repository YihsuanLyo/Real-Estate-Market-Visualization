import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from figure import *

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

control = dbc.Card([
    html.Div([
        dbc.Label("Invest Type"),
        dcc.Dropdown(
            id="invest_type",
            options=[
                {"label": col, "value": col} for col in ["房地产开发投资额(亿元)",
                                                         "房地产开发住宅投资额(亿元)",
                                                         "房地产开发别墅、高档公寓投资额(亿元)",
                                                         "房地产开发办公楼投资额(亿元)",
                                                         "房地产开发商业营业用房投资额(亿元)",
                                                         "房地产开发其他投资额(亿元)"]],
            value="房地产开发投资额(亿元)",
            clearable=False
        ),
    ]
    ),
    html.Div([
        dbc.Label("Invest Districts"),
        dcc.Dropdown(
            list(set(data["地区"])),
            id="districts",
            multi=True,
        ),
    ]
    ),
    html.Div([
        dbc.Label("Range of Years"),
        dcc.RangeSlider(2010, 2020, 1, value=[2010, 2020], id='years_range', pushable=1,
                        marks=dict(zip(range(2010, 2021), [str(e) for e in range(2010, 2021)]))),
    ]
    ),
    html.Div([
        dbc.Label("Investment Year"),
        dcc.Slider(2010, 2020, 1, value=2020, id='invest_year', included=False,
                   marks=dict(zip(range(2010, 2021), [str(e) for e in range(2010, 2021)]))),
    ]
    ),
],
    body=True,
)

children = [
    html.H1("Chinese Real Estate Investment"),
    html.Hr(),
    dbc.Row(
        [
            dbc.Col(control, md=4),
            dbc.Col(dcc.Graph(id="scatter-graph"), md=8),
        ],
        align="center",
    ),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id="pie-graph"), md=4),
            dbc.Col(dcc.Graph(id="map-graph"), md=8),
        ],
        align="center",
    ),
]

container = dbc.Container(
    children=children,
    id="container",
    fluid=True,
)

content = html.Div([container], id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    Output("scatter-graph", "figure"),
    [
        Input("invest_type", "value"),
        Input("districts", "value"),
        Input("years_range", "value"),
    ],
)
def make_scatter_graph(invest_type, district, year_range):
    return getInvestmentLineChart(invest_type, district, year_range)


@app.callback(
    Output("map-graph", "figure"),
    [
        Input("invest_type", "value"),
        Input("invest_year", "value"),
    ],
)
def make_map_graph(map_type, map_year):
    return getChineseMap(map_type, map_year)


@app.callback(
    Output("pie-graph", "figure"),
    [
        Input("districts", "value"),
        Input("invest_year", "value"),
    ],
)
def make_pie_graph(districts, year):
    return getInvestPieChart(districts, year)


@app.callback(Output("container", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return children
    else:
        return [
            html.H1("Chinese Real Estate Investment"),
            html.Hr(),
            html.H3("Here is %s!" % pathname)
        ]


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
