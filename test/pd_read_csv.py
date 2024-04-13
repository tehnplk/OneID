import pandas as pd
import csv

if __name__ == '__main__':

    df = pd.read_csv('./provider.txt',delimiter="\t")
    print(df)

    with open("provider.txt", "r", encoding="utf8") as tsv:
        data = csv.reader(tsv, delimiter="\t")
        datas = list()
        for row in data:
            datas.append(row)
        print(len(datas), datas)