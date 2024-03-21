from distutils.log import debug
from fileinput import filename
from flask import *
import pymysql
import pandas as pd

import configparser

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
def main():
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        if not f:
            return redirect('/')
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
        print(datas)

        with connection.cursor() as cursor:
            sql = "delete from data_raw"
            cursor.execute(sql)

            sql = "insert into data_raw (hoscode,hosname,region,prov,amp,tmb,device,ekyc_pop,ekyc_do,otp_confirm,emp_total,emp_confirm,emp_percent) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.executemany(sql, datas)

            sql = f"insert into log_file values (NULL,NOW(),'{f.filename}','{request.remote_addr}');";
            print(sql)
            cursor.execute(sql)

            cursor.execute("call Z_All_process();")
            connection.commit()

        return render_template("result.html", name=f.filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
