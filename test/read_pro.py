import csv
import configparser
import pymysql

config = configparser.ConfigParser()
config.read('../host_db.ini')
host = config.get('DB', 'host')
user = config.get('DB', 'user')
password = config.get('DB', 'password')
db = config.get('DB', 'db')
port = config.getint('DB', 'port')


connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port
        )

cursor = connection.cursor()


with open("provider.txt", "r", encoding="utf8") as tsv:
    data = csv.reader(tsv, delimiter="\t")
    print(type(data))
    datas = list()
    for row in data:
        datas.append(row)
    print(len(datas),datas)

    cursor.execute("truncate provider_raw");

    sql = "insert into provider_raw values (%s,%s,%s,%s,%s,0,%s,now())"
    cursor.executemany(sql, datas)
    connection.commit()
    cursor.close()
    connection.close()
