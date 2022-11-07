import json

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_excel("../year_data.xlsx", index_col=0)
no_margin_style = dict(l=0, r=0, t=0, b=0)

keys = {
    "房地产开发企业个数(个)": [
        "内资房地产开发企业个数(个)",
        "国有房地产开发企业个数(个)",
        "集体房地产开发企业个数(个)",
        "港、澳、台投资房地产开发企业个数(个)",
        "外商投资房地产开发企业个数(个)"
    ],
    "房地产开发企业平均从业人数(人)": [
        "港、澳、台投资房地产开发企业平均从业人数(人)",
        "外商投资房地产开发企业平均从业人数(人)",
        "内资房地产开发企业平均从业人数(人)",
        "国有房地产开发企业平均从业人数(人)",
        "集体房地产开发企业平均从业人数(人)"
    ],
    "房地产开发企业资产负债": [
        "房地产开发企业实收资本(亿元)",
        "房地产开发企业资产总计(亿元)",
        "房地产开发企业累计折旧(亿元)",
        "房地产开发企业本年折旧(亿元)",
        "房地产开发企业负债合计(亿元)",
        "房地产开发企业所有者权益(亿元)", ],
    "房地产开发企业资金来源": [
        "房地产开发企业本年实际到位资金(亿元)",
        "房地产开发企业国内贷款(亿元)",
        "房地产开发企业利用外资(亿元)",
        "房地产开发企业自筹资金(亿元)",
        "房地产开发企业其他资金来源(亿元)"],
    "房地产开发企业经营情况": [
        "房地产开发企业主营业务收入(亿元)",
        "房地产开发企业土地转让收入(亿元)",
        "房地产开发企业商品房销售收入(亿元)",
        "房地产开发企业房屋出租收入(亿元)",
        "房地产开发企业其他收入(亿元)",
        "房地产开发企业主营业务税金及附加(亿元)",
        "房地产开发企业营业利润(亿元)"]
}


def getLineChartPage1(district=None):
    if not district:
        district = "全国"
    components = []
    t = data[data["地区"].str.contains(district)]
    # print(t[["房地产开发企业个数(个)", "房地产开发企业平均从业人数(人)"]])
    components.append(go.Scatter(x=t["年份"], y=t["房地产开发企业个数(个)"],
                                 mode="lines+markers", name="房地产开发企业个数(个)", showlegend=True,
                                 xaxis="x", yaxis="y1"))
    components.append(go.Scatter(x=t["年份"], y=t["房地产开发企业平均从业人数(人)"],
                                 mode="lines+markers", name="房地产开发企业平均从业人数(个)", showlegend=True,
                                 xaxis="x", yaxis="y2"))

    fig = go.Figure(components)

    fig.update_layout(
        yaxis2=dict(anchor="x", overlaying="y", side="right"),
        xaxis=dict(dtick=1),
        margin=no_margin_style,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    return fig


def getPieChart1Page1(district=None, year=None, flag=0):
    if not district:
        district = "全国"
    if not year:
        year = 2015
    key = keys["房地产开发企业个数(个)"] if flag else keys["房地产开发企业平均从业人数(人)"]
    t = data[(data["地区"].str.contains(district)) & (data["年份"] == year)]

    labels = [e for e in key]
    values = [v for e in key for v in t[e]]
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=labels, values=values, showlegend=False))
    fig.update_layout(
        margin=no_margin_style, width=200, height=200,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


def getTreeMapPage1(district=None, year=None, ):
    if not district:
        district = "全国"
    if not year:
        year = 2015
    t = data[(data["地区"].str.contains(district)) & (data["年份"] == year)]

    fig = make_subplots(
        cols=3, rows=1,
        column_widths=[0.4, 0.4, 0.4],
        specs=[[{'type': 'treemap'}, {'type': 'treemap'}, {'type': 'treemap'}]],
        horizontal_spacing=0
    )

    colors = ["lightblue", "lightgrey", "lightgreen"]
    for i, key in enumerate(["房地产开发企业资产负债", "房地产开发企业资金来源", "房地产开发企业经营情况"]):
        labels = [key] + keys[key]
        parents = [""] + [key] * len(keys[key])
        values = [0] + [v for e in keys[key] for v in t[e]]

        fig.add_trace(go.Treemap(labels=labels, parents=parents, values=values,
                                 marker_colors=[colors[i]] * len(values)),
                      row=1, col=i + 1)

    fig.update_layout(margin=no_margin_style)
    return fig


def getInvestmentLineChart(invest_type="房地产开发投资额(亿元)", district=None, year_range=(2010, 2020)):
    components = []
    if district:
        for e in district:
            t = data[(data["地区"].str.contains(e))
                     & (year_range[0] <= data["年份"])
                     & (data["年份"] <= year_range[1])]
            components.append(go.Scatter(x=t["年份"], y=t[invest_type],
                                         mode="lines+markers", name=e, showlegend=True))
    else:
        t = data[(data["地区"].str.contains("全国"))
                 & (year_range[0] <= data["年份"])
                 & (data["年份"] <= year_range[1])]
        components.append(go.Scatter(x=t["年份"], y=t[invest_type],
                                     mode="lines+markers", name="全国", showlegend=True))

    fig = go.Figure(components)
    fig.update_layout(
        xaxis=dict(dtick=1)
    )
    return fig


def getChineseMap(name=None, year=None):
    with open(r'./china_geojson/china.json', encoding='utf8') as js:
        geo = json.load(js)
    t = data[(data["年份"] == year) & (data["地区"] != "全国")]
    zmax, zmin = max(data[data["地区"] != "全国"][name]), min(data[data["地区"] != "全国"][name])
    fig = go.Figure()
    fig.add_trace(go.Choroplethmapbox(geojson=geo,
                                      featureidkey="properties.name",
                                      locations=t["地区"],
                                      z=t[name],
                                      colorscale="OrRd",
                                      zmax=zmax, zmin=zmin
                                      )
                  )
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3, mapbox_center={"lat": 35.9, "lon": 104.2})
    fig.update_layout(margin=no_margin_style)
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
    # print("\"", "\",\n\"".join(e for e in data.keys() if "" in e), "\"", sep="")
    getTreeMapPage1().show()
