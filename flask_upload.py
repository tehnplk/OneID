from distutils.log import debug
from fileinput import filename
from flask import *
import pymysql
import pandas as pd
from openpyxl import workbook, load_workbook
import configparser

import csv

from datetime import datetime

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('host_db.ini')
host = config.get('DB', 'host')
user = config.get('DB', 'user')
password = config.get('DB', 'password')
db = config.get('DB', 'db')
port = config.getint('DB', 'port')
print(host)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/idx_health_id')
def up_health_id():
    return render_template("healthid.html")


@app.route('/idx_provider_id')
def up_provider_id():
    return render_template("providerid.html")

@app.route('/idx_phr')
def up_phr():
    return render_template("phr.html")


@app.route('/do_health_id', methods=['POST'])
def do_health_id():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return redirect('/idx_health_id')
        f.save(f"./upload/{f.filename}")

        df = pd.read_excel(f"./upload/{f.filename}")

        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port
        )

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
        # print(datas)

        with connection.cursor() as cursor:
            sql = "delete from data_raw"
            cursor.execute(sql)

            sql = "insert into data_raw (hoscode,hosname,region,prov,amp,tmb,device,ekyc_pop,ekyc_do,otp_confirm,emp_total,emp_confirm,emp_percent) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.executemany(sql, datas)

            sql = f"insert into log_file values (NULL,NOW(),'{f.filename}','{request.remote_addr}');";

            cursor.execute(sql)

            cursor.execute("call B_All_process();")
            connection.commit()
            print(datetime.now(), "upload health_id")

        return render_template("result.html", name=f.filename)


@app.route('/do_provider_id', methods=['POST'])
def do_provider_id():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return redirect('/idx_provider_id')
        f.save(f"./upload/{f.filename}")

        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port
        )

        cursor = connection.cursor()

        with open(f"./upload/{f.filename}", "r", encoding="utf8") as tsv:
            data = csv.reader(tsv, delimiter="\t")
            print(type(data))
            datas = list()
            for row in data:
                datas.append(row)
            # print(len(datas), datas)

            cursor.execute("truncate provider_raw");

            sql = "insert into provider_raw values (%s,%s,%s,%s,%s,0,%s,now())"
            cursor.executemany(sql, datas)

            sql = f"insert into log_file values (NULL,NOW(),'{f.filename}','{request.remote_addr}');"
            cursor.execute(sql)
            cursor.execute("call C_All_process();")
            connection.commit()
            print(datetime.now(), "upload provider_id")

        return render_template("result.html", name=f.filename)

@app.route('/do_phr', methods=['POST'])
def do_phr():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return redirect('/idx_phr')
        f.save(f"./upload/{f.filename}")

        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port
        )

        wb = load_workbook(f"./upload/{f.filename}")
        ws = wb.active

        i = 0

        datas = list()
        for row in ws:
            cells = []
            for c in row:
                val = str(c.value).replace('\n', '')
                if val == 'None':
                    val = None
                cells.append(val)
            cells = tuple(cells)
            datas.append(cells)
        datas.pop(0)

        print('import .. ', len(datas))

        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE phr_raw;")
            sql = "insert into phr_raw values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.executemany(sql, datas)
            connection.commit()


        return render_template("result.html", name=f.filename)



if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
