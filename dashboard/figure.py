import json

import pandas as pd
import plotly.graph_objects as go

data = pd.read_excel("../data.xlsx", index_col=0)


def getInvestmentLineChart(invest_type="房地产开发投资额(亿元)", district=None, year_range=(2010, 2020)):
    components = []
    if district:
        for e in district:
            t = data[(data["地区"].str.contains(e))
                     & (year_range[0] <= data["年份"])
                     & (data["年份"] <= year_range[1])]
            components.append(go.Scatter(x=t["年份"], y=t[invest_type],
                                         mode="lines", name=e, showlegend=True))
    else:
        t = data[(year_range[0] <= data["年份"]) &
                 (data["年份"] <= year_range[1])].groupby("年份", as_index=False)[invest_type].agg(sum)
        components.append(
            go.Scatter(
                x=t["年份"],
                y=t[invest_type],
                mode="lines",
                name="全国",
                showlegend=True
            )
        )
    fig = go.Figure(components)
    fig.update_layout(
        xaxis=dict(dtick=1)
    )
    return fig


def getChineseMap(name=None, year=None):
    with open(r'./china_geojson/china.json', encoding='utf8') as js:
        geo = json.load(js)
    t = data[data["年份"] == year]
    fig = go.Figure()
    fig.add_trace(go.Choroplethmapbox(geojson=geo,
                                      featureidkey="properties.name",
                                      locations=t["地区"],
                                      z=t[name],
                                      )
                  )
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3, mapbox_center={"lat": 35.9, "lon": 104.2})
    fig.update_layout(margin={"t": 0, "b": 0, "l": 0, "r": 0})
    return fig


def getInvestPieChart(districts=None, year=2020):
    keys = ["房地产开发住宅投资额(亿元)",
            "房地产开发别墅、高档公寓投资额(亿元)",
            "房地产开发办公楼投资额(亿元)",
            "房地产开发商业营业用房投资额(亿元)",
            "房地产开发其他投资额(亿元)"]
    if not districts:
        districts = set(data["地区"])
    t = data[(data["地区"].isin(districts)) & (data["年份"] == year)][keys]

    labels = [e[5:-4] for e in keys]
    values = [t[e].sum() for e in keys]

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=labels, values=values))
    return fig


if __name__ == '__main__':
    getInvestPieChart(["广东省", "北京市"], 2015).show()
