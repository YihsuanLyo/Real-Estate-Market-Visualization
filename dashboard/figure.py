import json

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_excel("../year_data.xlsx", index_col=0)
general_style = dict(margin=dict(l=2, r=2, t=2, b=2), autosize=True)

def allDistricts():
    districts = set(data["地区"])
    districts.remove("全国")
    return list(districts)

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


def convertProvince(s):
    return s[:3] if s[0] in ["内", "黑"] else s[:2]


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
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        **general_style
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
        margin=general_style["margin"], width=200, height=200,
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

    fig.update_layout(**general_style)
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
    fig.update_layout(**general_style)
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


class DevelopmentPage():
    def __init__(self):
        self.keys = {
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
            "房地产开发企业总收入(亿元)": ["房地产开发企业主营业务收入(亿元)",
                                           "房地产开发企业土地转让收入(亿元)",
                                           "房地产开发企业商品房销售收入(亿元)",
                                           "房地产开发企业房屋出租收入(亿元)",
                                           "房地产开发企业其他收入(亿元)"]
        }

    def getLineChart(self, district="全国", names=None):
        if not names:
            names = [""]
        t = data[data["地区"].str.contains(district)]
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=t["年份"],
                                 y=t[[name + "房地产开发企业个数(个)" for name in names]].sum(axis=1),
                                 mode="lines+markers",
                                 name="房地产开发企业个数(个)",
                                 showlegend=True,
                                 xaxis="x", yaxis="y1"))
        fig.add_trace(go.Scatter(x=t["年份"],
                                 y=t[[name + "房地产开发企业平均从业人数(人)" for name in names]].sum(axis=1),
                                 name="房地产开发企业平均从业人数(人)",
                                 showlegend=True, mode="lines+markers",
                                 xaxis="x", yaxis="y2"))
        fig.update_layout(
            yaxis2=dict(anchor="x", overlaying="y", side="right"),
            xaxis=dict(dtick=1),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.12,
                xanchor="right",
                x=1
            ),
            **general_style
        )
        return fig

    def getBarChart(self, year=2020, building_types=None, name="房地产开发企业个数(个)", descending=False):
        assert name in ["房地产开发企业个数(个)", "房地产开发企业平均从业人数(人)"]
        if not building_types:
            building_types = [""]

        colors_dict = {"": "lightblue", "内资": "blue", "国有": "red",
                       "集体": "lightgreen", "港、澳、台投资": "purple", "外商投资": "orange"}

        keys = [e + name for e in building_types]
        fig = go.Figure()
        t = data[(data["年份"] == year) & (data["地区"] != "全国")]
        t.insert(1, "sum", t[keys].sum(axis=1), allow_duplicates=False)
        t = t.sort_values(["sum", "地区"], ascending=descending)
        for key in keys:
            fig.add_trace(go.Bar(x=t[key][len(t[key]) // 2:],
                                 y=[convertProvince(e) for e in t["地区"][len(t[key]) // 2:]],
                                 orientation="h",
                                 name=key[:key.index("房")],
                                 marker_color=colors_dict[key[:-len(name)]]))

        fig.update_layout(
            barmode="stack",
            xaxis=dict(range=[0, 1.1 * max(t["sum"])]),
            **general_style
        )

        return fig

    def getStackedChart(self, district="全国"):
        t = data[data["地区"].str.contains(district)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t["年份"], y=t["房地产开发企业负债合计(亿元)"],
                                 name="房地产开发企业负债合计(亿元)", showlegend=True,
                                 mode="lines", fill="tozeroy",
                                 xaxis="x", yaxis="y1"))
        fig.add_trace(go.Scatter(x=t["年份"], y=t["房地产开发企业资产总计(亿元)"],
                                 name="房地产开发企业所有者权益(亿元)", showlegend=True,
                                 mode="lines", fill="tonexty",
                                 xaxis="x", yaxis="y1"))
        fig.add_trace(go.Scatter(x=t["年份"], y=t["房地产开发企业负债合计(亿元)"] / t["房地产开发企业资产总计(亿元)"],
                                 name="房地产开发企业资产负债率(%)", showlegend=True,
                                 mode="lines+markers",
                                 xaxis="x", yaxis="y2"))
        fig.update_layout(
            xaxis=dict(dtick=1),
            # yaxis1=dict(range=[]),
            yaxis2=dict(anchor="x", overlaying="y", side="right", range=[0, 1]),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            **general_style
        )
        return fig

    def getPieChart(self, district="全国", year=2020, name="房地产开发企业个数(个)"):
        assert name in self.keys
        if not district:
            district = "全国"
        if not year:
            year = 2020
        keys = self.keys[name]
        t = data[(data["地区"].str.contains(district)) & (data["年份"] == year)]

        labels = [e for e in keys]
        values = [v for e in keys for v in t[e]]
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=labels, values=values, showlegend=True, hole=0.3))
        fig.update_layout(
            **general_style
        )
        return fig

    def getBubbleChart(self, districts=None):
        if not districts:
            districts = set(data["地区"])
            districts.remove("全国")
        keys = self.keys["房地产开发企业总收入(亿元)"]

        fig = go.Figure()
        for district in districts:
            t = data[data["地区"].str.contains(district)]
            income = t[keys].sum(axis=1)
            profit = t["房地产开发企业营业利润(亿元)"]
            cost = income - profit - t["房地产开发企业主营业务税金及附加(亿元)"]
            fig.add_trace(go.Scatter(x=t["年份"],
                                     y=profit / (income - profit),
                                     name=convertProvince(district),
                                     mode="markers",
                                     marker=dict(size=income,
                                                 sizemode='area',
                                                 sizeref=5,
                                                 sizemin=1, )
                                     ))
        fig.update_layout(**general_style)
        return fig


class SalePage():
    def __init__(self):
        self.keys = {
            "商品房": [
                "住宅商品房",
                "别墅、高档公寓",
                "办公楼商品房",
                "商业营业用房",
                "其他商品房"
            ],
            "指标": [
                "销售面积(万平方米)",
                "销售额(亿元)",
                "平均销售价格(元/平方米)"
            ],
            "竣工与销售": ["住宅", "别墅、高档公寓"]
        }
        with open(r'./china_geojson/china.json', encoding='utf8') as js:
            self.geoInfo = json.load(js)

    def getGeoMap(self, building_types=None, name="销售面积(万平方米)", year=2020):
        assert name in self.keys["指标"]
        if not building_types:
            building_types = ["商品房"]
        keys = [e + name for e in building_types]

        t = data[data["地区"] != "全国"]
        t.insert(1, "sum", t[keys].sum(axis=1), allow_duplicates=False)
        zmax, zmin = max(t["sum"]), min(t["sum"])
        t = t[t["年份"] == year]

        fig = go.Figure()
        fig.add_trace(go.Choroplethmapbox(geojson=self.geoInfo,
                                          featureidkey="properties.name",
                                          locations=t["地区"],
                                          z=t["sum"],
                                          colorscale="OrRd",
                                          zmax=zmax, zmin=zmin
                                          )
                      )
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=2.6,
            mapbox_center={"lat": 35.9, "lon": 104.2},
            **general_style
        )
        return fig

    def getStackedChart(self, name="销售面积(万平方米)", building_types=None, district=None):
        assert name in self.keys["指标"]
        if not district:
            district = "全国"
        if not building_types:
            building_types = ["商品房"]

        t = data[data["地区"].str.contains(district)]
        accumulate = t[building_types[0] + name]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t["年份"], y=accumulate,
                                 name=building_types[0], showlegend=True,
                                 mode="none", fill="tozeroy", ))

        for building_type in building_types[1:]:
            accumulate += t[building_type + name]
            fig.add_trace(go.Scatter(x=t["年份"], y=accumulate,
                                     name=building_type, showlegend=True,
                                     mode="none", fill="tonexty", ))

        t = data[data["地区"] == "全国"] if district == "全国" else data[data["地区"] != "全国"]
        accumulate = t[[e + name for e in building_types]].sum(axis=1)
        ymax = max(accumulate)

        fig.update_layout(
            xaxis=dict(dtick=1),
            yaxis=dict(range=[0, ymax]),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            **general_style
        )
        return fig

    def getAveragePriceTable(self, districts=None, building_type=None):
        districts = ["全国"] + districts if districts else ["全国"]
        if not building_type:
            building_type = "商品房"
        assert building_type == "商品房" or building_type in self.keys["商品房"]

        years = data[data["地区"] == districts[0]]["年份"]

        fig = go.Figure(go.Table(
            header=dict(values=["年份"] + [convertProvince(e) for e in districts]),
            cells=dict(values=[years] + [data[data["地区"] == district][building_type + "平均销售价格(元/平方米)"]
                                         for district in districts]),
        ))

        fig.update_layout(
            title="平均销售价格(元/平方米)",
            # **general_style
        )
        return fig

    def getAveragePriceBar(self, districts=None, building_type=None):
        districts = ["全国"] + districts if districts else ["全国"]
        if not building_type:
            building_type = "商品房"
        assert building_type == "商品房" or building_type in self.keys["商品房"]

        fig = go.Figure()
        for district in districts:
            t = data[data["地区"] == district]
            fig.add_trace(go.Bar(x=t["年份"], y=t[building_type + "平均销售价格(元/平方米)"], name=district))
        fig.update_layout(
            barmode="group",
            **general_style
        )
        return fig


    def getScatterChart(self, name="住宅"):
        assert name in self.keys["竣工与销售"]
        districts = set(data["地区"])
        districts.remove("全国")
        shapes = ["circle", "square", "diamond", "cross", "x", "triangle-up",
                  "pentagon", "hexagram", "star", "diamond", "hourglass"]

        fig = go.Figure()

        # for year in set(data["年份"]):
        #     t = data[(data["地区"].isin(districts)) & (data["年份"] == year)]
        #     fig.add_trace(go.Scatter(
        #         x=t["房地产开发企业%s销售套数(套)" % name],
        #         y=t["房地产开发企业%s竣工套数(套)" % name],
        #         name=str(year),
        #         # marker=dict(symbol=shapes[:len(t["年份"])]),
        #         showlegend=True,
        #         mode="markers",
        #     ))

        for district in districts:
            t = data[data["地区"] == district]
            fig.add_trace(go.Scatter(
                x=t["房地产开发企业%s销售套数(套)" % name],
                y=t["房地产开发企业%s竣工套数(套)" % name],
                name=convertProvince(district),
                marker=dict(symbol=shapes[:len(t["年份"])]),
                showlegend=False,
                mode="markers",
            ))

        if name == "住宅":
            fig.add_trace(go.Scatter(
                x=[0, 820000], y=[0, 820000], mode="lines",
                line=dict(color='royalblue', width=2, dash='dash'),
                showlegend=False
            ))
        else:
            fig.add_trace(go.Scatter(
                x=[0, 30000], y=[0, 30000], mode="lines",
                line=dict(color='royalblue', width=2, dash='dash'),
                showlegend=False
            ))
            fig.update_layout(
                xaxis=dict(range=[0, 45000]),
                yaxis=dict(range=[0, 30000])
            )

        fig.update_layout(
            **general_style,
        )
        return fig


class InvestmentPage():
    def __init__(self):
        self.keys = {
            "资金来源": [
                "房地产开发企业国内贷款(亿元)",
                "房地产开发企业自筹资金(亿元)",
                "房地产开发企业利用外资(亿元)",
                "房地产开发企业其他资金来源(亿元)",
            ],
            "资金用途": [
                "房地产开发企业建筑安装工程本年完成投资额(亿元)",
                "房地产开发企业设备工器具购置本年完成投资额(亿元)",
                "房地产开发企业其他费用本年完成投资额(亿元)",
            ],
            "建筑类型": [
                "房地产开发住宅投资额(亿元)",
                "房地产开发别墅、高档公寓投资额(亿元)",
                "房地产开发办公楼投资额(亿元)",
                "房地产开发商业营业用房投资额(亿元)",
                "房地产开发其他投资额(亿元)",
            ],
            "项目规模": [
                "500万元以下房地产开发投资额(亿元)",
                "500-1000万元房地产开发投资额(亿元)",
                "1000-3000万元房地产开发投资额(亿元)",
                "3000-5000万元房地产开发投资额(亿元)",
                "5000万-1亿元房地产开发投资额(亿元)",
                "1-5亿元房地产开发投资额(亿元)",
                "5-10亿元房地产开发投资额(亿元)",
                "10亿元以上房地产开发投资额(亿元)"
            ],
            "房地产开发企业新开工房屋面积(万平方米)": [
                "房地产开发企业住宅新开工房屋面积(万平方米)",
                "房地产开发企业别墅、高档公寓新开工房屋面积(万平方米)",
                "房地产开发企业办公楼新开工房屋面积(万平方米)",
                "房地产开发企业商业营业用房新开工房屋面积(万平方米)",
                "房地产开发企业其他用途新开工房屋面积(万平方米)"
            ]
        }

    def getBarChartWithLine(self, x, y1, y2, ly, y1_name, y2_name, line_name, district=None):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x,
            y=y1,
            name=y1_name,
            xaxis="x", yaxis="y1"
        ))
        fig.add_trace(go.Bar(
            x=x,
            y=y2,
            name=y2_name,
            xaxis="x", yaxis="y1"
        ))
        fig.add_trace(go.Scatter(
            x=x,
            y=ly,
            mode="lines+markers",
            xaxis="x", yaxis="y2",
            name=line_name
        ))

        fig.update_layout(
            barmode="group",
            yaxis2=dict(anchor="x", overlaying="y", side="right", range=[0, 1]),
            xaxis=dict(dtick=1),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            **general_style
        )

        return fig

    def getInvestmentPlanChart(self, district=None):
        if not district:
            district = "全国"
        t = data[data["地区"] == district]

        x, y1, y2 = t["年份"], t["房地产开发企业计划总投资(亿元)"], t[
            "房地产开发企业自开始建设至本年底累计完成投资(亿元)"]
        return self.getBarChartWithLine(
            x, y1, y2, y2 / y1,
            "房地产开发企业计划总投资(亿元)", "房地产开发企业已完成投资(亿元)", "房地产开发企业已完成投资占比(%)",
            district
        )

    def getConstructingAreaChart(self, district=None):
        if not district:
            district = "全国"
        t = data[data["地区"] == district]

        x, y1, y2 = t["年份"], t["房地产开发企业施工房屋面积(万平方米)"], t["房地产开发企业竣工房屋面积(万平方米)"]
        return self.getBarChartWithLine(
            x, y1, y2, y2 / y1,
            "房地产开发企业施工房屋面积(万平方米)", "房地产开发企业竣工房屋面积(万平方米)",
            "房地产开发企业房屋建筑面积竣工率(%)",
            district
        )

    def getConstructingValueChart(self, district=None):
        if not district:
            district = "全国"
        t = data[data["地区"] == district]

        x, y1 = t["年份"], t["房地产开发企业竣工房屋价值(亿元)"]
        y2 = t["房地产开发企业竣工房屋造价(元/平方米)"] * t["房地产开发企业竣工房屋面积(万平方米)"] / 10000
        return self.getBarChartWithLine(
            x, y1, y2, (y1 - y2) / y2,
            "房地产开发企业竣工房屋价值(亿元)", "房地产开发企业竣工房屋造价(元/平方米)",
            "房地产开发企业竣工房屋增值占比(%)",
            district
        )

    def getInvestmentTreemap(self, district=None, year=2015):
        if not district:
            district = "全国"
        t = data[(data["地区"].str.contains(district)) & (data["年份"] == year)]

        labels, parents, values = ["资金来源", "资金用途"], ["", ""], [0, 0]
        for e in ["资金来源", "资金用途"]:
            labels += self.keys[e]
            parents += [e] * len(self.keys[e])
            values += [v for l in self.keys[e] for v in t[l]]

        fig = go.Figure(go.Treemap(labels=labels, parents=parents, values=values, ))
        fig.update_layout(**general_style)
        return fig

    def getInvestmentTable(self, year=2020, district=None, name="项目规模"):
        if not district:
            district = "全国"
        assert name in ["项目规模", "建筑类型"]

        t = data[(data["地区"] == district) & (data["年份"] == year)]

        keys = self.keys[name]
        values = [v for key in keys for v in t[key]]

        percentages = []
        for e in values:
            e = e * 100 / sum(values)
            percentages.append(round(e, 2))
            i = 3
            while not percentages[-1]:
                percentages[-1] += round(e, i)
                i += 1

        fig = go.Figure(go.Table(
            header=dict(values=[name, "投资额", "占比"]),
            cells=dict(values=[keys, values, percentages]),
        ))
        fig.update_layout(**general_style)
        return fig

    def getNewConstructionPie(self, year=2020, district=None):
        if not district:
            district = "全国"

        keys = self.keys["房地产开发企业新开工房屋面积(万平方米)"]
        t = data[(data["地区"] == district) & (data["年份"] == year)]

        labels = [e for e in keys]
        values = [v for e in keys for v in t[e]]
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=labels, values=values, showlegend=False))
        fig.update_layout(
            margin=general_style["margin"],
            # width=200, height=200,
            # paper_bgcolor='rgba(0,0,0,0)',
            # plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig


if __name__ == '__main__':
    print("\"", "\",\n\"".join(e for e in data.keys() if "销售面积" in e), "\"", sep="")

    page = SalePage()
    page.getAveragePriceBar().show()
