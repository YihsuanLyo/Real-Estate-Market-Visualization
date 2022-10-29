import pandas as pd

def read_data(file):
    return pd.read_excel(file, index_col=0)


if __name__ == '__main__':
    data = read_data("../data.xlsx")
    print(data)
