import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, dash_table
from dash.exceptions import PreventUpdate

from figure import *

PIE_WINDOW_STYLE = {"position": "absolute", "left": "1100px", "top": "300px"}


def getDataTable(district="全国", name="房地产开发企业个数(个)"):
    if not district or not name:
        return dash_table.DataTable()
    key = ["年份"] + keys[name]
    if name in data.keys():
        key.insert(1, name)
    t = data[data["地区"].str.contains(district)][key]
    return dash_table.DataTable(columns=[{"name": i, "id": i} for i in t.columns],
                                data=t.to_dict('records'), )


app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])

children = [
    html.H1("房地产公司经营情况"),
    html.Hr(),
    dbc.Row(dcc.Dropdown(id="district",
                         options=[{"label": e, "value": e} for e in set(data["地区"])],
                         value="全国",
                         clearable=False)),
    html.Div(dcc.Graph(id="scatter", figure=getLineChartPage1())),
    html.Div(dcc.Graph(id="pie", figure=getPieChart1Page1()),
             id="PieWindow", style=PIE_WINDOW_STYLE),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id="treemap", figure=getTreeMapPage1()), width=12),
            # dbc.Col([
            #     dbc.Row(dcc.Dropdown(id="district",
            #                          options=[{"label": e, "value": e} for e in set(data["地区"])],
            #                          value="全国",
            #                          clearable=False)),
            #     dbc.Row(getDataTable(), id="table", )
            # ],
            #     width=4)
        ],
    ),
    dbc.Row(getDataTable(), id="table", )
]

app.layout = dbc.Container(children)


@app.callback(
    Output("scatter", "figure"),
    Input("district", "value"),
)
def make_pie_graph(district):
    return getLineChartPage1(district)


@app.callback(
    [Output("pie", "figure"),
     Output("treemap", "figure")],
    [Input("scatter", "clickData"),
     Input("district", "value")],
)
def make_pie_graph(click_data, district):
    if not click_data:
        raise PreventUpdate

    point = click_data["points"][0]
    year = point["x"]
    flag = point["curveNumber"]

    return getPieChart1Page1(district=district, year=year, flag=flag), getTreeMapPage1(district=district, year=year)


click_cache = {"scatter": None, "treemap": None, "current_showing": None}


@app.callback(
    Output("table", "children"),
    [Input("district", "value"),
     Input("treemap", "clickData"),
     Input("scatter", "clickData")],
)
def make_pie_graph(district, treemap_click, scatter_click):
    print("\n", district, treemap_click, scatter_click, sep="\n")
    if not treemap_click and not scatter_click:
        raise PreventUpdate
    if treemap_click and str(treemap_click) != click_cache["treemap"]:
        click_cache["treemap"] = str(treemap_click)
        name = treemap_click["points"][0]["parent"] or treemap_click["points"][0]["root"]
    elif scatter_click and str(scatter_click) != click_cache["scatter"]:
        click_cache["scatter"] = str(scatter_click)
        name = "房地产开发企业平均从业人数(人)" if scatter_click["points"][0]["curveNumber"] else "房地产开发企业个数(个)"
    elif click_cache["current_showing"]:
        name = click_cache["current_showing"]
    else:
        raise ValueError

    click_cache["current_showing"] = name
    return getDataTable(district=district, name=name)


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
