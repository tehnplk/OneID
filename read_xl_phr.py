from openpyxl import workbook, load_workbook
import configparser
import pymysql

config = configparser.ConfigParser()
config.read('host_db.ini')
host = config.get('DB', 'host')
user = config.get('DB', 'user')
password = config.get('DB', 'password')
db = config.get('DB', 'db')
port = config.getint('DB', 'port')
print(host)

if __name__ == '__main__':

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        port=port
    )

    wb = load_workbook("./xls/phr.xlsx")
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

    print('import .. ',len(datas))


    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE phr_raw;")
        sql = "insert into phr_raw values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.executemany(sql, datas)
        connection.commit()

