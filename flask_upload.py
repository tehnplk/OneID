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

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    db=db,
    port=port
)


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


@app.route('/idx_telemed')
def up_telemed():
    return render_template("telemed.html")


@app.route('/idx_appointment')
def up_appointment():
    return render_template("appointment.html")


@app.route('/do_health_id', methods=['POST'])
def do_health_id():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return redirect('/idx_health_id')
        f.save(f"./upload/{f.filename}")

        wb = load_workbook(f"./upload/{f.filename}")
        ws = wb.active
        ws.delete_cols(1, 1)
        ws.delete_cols(3, 2)
        ws.delete_cols(14, 10)
        datas = []
        for row in ws:
            data_row = []
            for cell in row:
                c = cell.value
                if c is None:
                    c = ''
                data_row.append(str(c))
            datas.append(data_row)
            # print(data_row)
        datas.pop(0)

        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            port=port
        )

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


@app.route('/do_telemed', methods=['POST'])
def do_telemed():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return redirect('/idx_telemed')
        f.save(f"./upload/{f.filename}")

        with open(f"./upload/{f.filename}", "r", encoding="utf8") as file_stream:
            data = csv.reader(file_stream, delimiter=",")
            rows = list()
            for row in data:
                rows.append(row)

            rows.pop(0)
            datas = list()
            for r in rows:
                hos = r[0]
                hos = hos.split(":")
                hoscode = hos[0]
                hosname = hos[1]
                visit = r[1]
                m = [hoscode, hosname, visit]
                m = tuple(m)
                datas.append(m)

        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE telemed_raw;")
            sql = "insert into telemed_raw values (%s,%s,%s)"
            cursor.executemany(sql, datas)
            connection.commit()

        return render_template("result.html", name=f.filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
