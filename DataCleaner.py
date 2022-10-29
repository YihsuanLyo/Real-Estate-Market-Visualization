import os
import math
import pandas

if __name__ == '__main__':
    label = ["地区", "年份"]
    years = list(range(2010, 2021))
    districts = ['北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省',
                 '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省', '山东省', '河南省', '湖北省',
                 '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆市', '四川省', '贵州省', '云南省',
                 '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区']

    dic = dict()
    for district in districts:
        dic[district] = dict()
        for year in years:
            dic[district][year] = [district, year]

    for file in os.listdir("./dataset"):

        file = "./dataset/%s" % file
        data = pandas.read_excel(file)
        l = [data[e].tolist() for e in data]
        # print(l)

        name = l[0][0][3:]
        label.append(name)

        assert l[0][3:-1] == districts
        for temp in l[1:]:
            year = int(temp[2][:-1])
            assert year in years
            values = temp[3:-1]
            assert len(values) == len(districts)
            for i, v in enumerate(values):
                district = districts[i]
                dic[district][year].append(0 if v == "nan" or math.isnan(v) else float(v))

    print(label)
    print()
    # for district in districts:
    #     for year in years:
    #         assert len(dic[district][year]) == len(label)
    #         print(district, year, dic[district][year])
    data = pandas.DataFrame([dic[district][year] for year in years for district in districts],
                            columns=label, dtype=float)
    print(data)
    data.to_excel("./data.xlsx")
