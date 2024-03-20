import pandas as pd
import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password="112233",
    db='reportdid',
    port=3306
)

df = pd.read_excel('ekyc_hospital_summary_095020.xlsx')

datas = list()
for i in range(len(df)):
    rows = list()
    for n in range(1, 14):
        col = df.iloc[i, n]
        if n == 1:
            col = f"00000{str(df.iloc[i, n])}"
            col = col[-5:]
        rows.append(str(col))
    rows = tuple(rows)
    datas.append(rows)
print(datas)

with connection.cursor() as cursor:
    sql = "delete from data_raw"
    cursor.execute(sql)
    sql = "insert into data_raw  values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql, datas)

    cursor.execute("call Z_All_process();")
    connection.commit()
