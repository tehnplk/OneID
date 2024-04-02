import os
import sys
import requests
import time
import pymysql
from pymysql.constants import CLIENT

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QMessageBox, \
    QFileDialog, QDialog
from PyQt5.QtCore import QThread, QTimer, QEventLoop, pyqtSignal, QSettings, QObject
from PyQt5.QtGui import QIcon

from PyQt5 import uic, QtCore

from io import StringIO
import re
import csv
import version


def my_excepthook(type, value, tback):
    print(type, value, tback)
    sys.__excepthook__(type, value, tback)


def update_check(cid, resp, cur, conn):
    msg = str(resp['Message']).replace("'", "")
    result = str(resp['result']).replace("'", "")
    sql = f"update plk_moph_id_person_check set last_check_at = NOW(),last_message = '{msg}',moph_id_check_result = '{result}' where cid = '{cid}'"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    print(f'update for {cid}')


def read(txt):
    with open(txt, 'r') as f:
        r = f.read()
        return r.strip()


class Worker(QThread):
    sign_done = pyqtSignal()
    sign_err = pyqtSignal(dict)
    sign_progress = pyqtSignal(dict)

    def __init__(self):
        super(Worker, self).__init__()
        self.settings = QSettings("db_config.ini", QSettings.IniFormat)

        self.moo = None
        self.running = True

    def stop(self):
        self.running = False
        self.terminate()

    def run(self):
        url = """https://phr1.moph.go.th/idp/api/check_ekyc"""
        auth_token = read('./token.txt')
        headers = {'Authorization': f'Bearer {auth_token}'}

        conn = pymysql.connect(
            host=self.settings.value('DB/host'),
            user=self.settings.value('DB/user'),
            password=self.settings.value('DB/password'),
            db=self.settings.value('DB/db'),
            port=int(self.settings.value('DB/port')),
            charset='tis620',
            client_flag=CLIENT.MULTI_STATEMENTS,
            autocommit=False, )

        cur = conn.cursor(pymysql.cursors.DictCursor)

        sql = read('./sql_list_person.sql')
        if self.moo != 'All':
            sql = f"""{sql} and moo = '{self.moo}'"""
        print(sql)
        cur.execute(sql)
        persons = cur.fetchall()
        n = len(persons)
        print(f"Person = {n}")
        i = 0
        for p in persons:
            i += 1
            cid = p['cid']
            data = {'cid': cid}
            response = requests.post(url, json=data, headers=headers)
            resp = response.json()
            # print(f"{i}/{n}", ' --> ', cid, resp)
            if resp['MessageCode'] == 200:
                update_check(cid, resp, cur, conn)
                self.sign_progress.emit({'i': i, 'n': n, 'cid': cid, 'resp': resp})
            else:
                self.sign_err.emit(resp)
                print(resp)
            time.sleep(.2)
            QApplication.processEvents()

        self.sign_done.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('check_moph_id.ui', self)
        self.setWindowTitle(f"PLK Health ID Checker {version.ver()}")
        self.progressBar.setValue(0)

        self.btn_begin.clicked.connect(self.worker_begin)
        self.btn_config.clicked.connect(self.db_config)
        self.btn_token.clicked.connect(self.token)

        self.btn_excel.clicked.connect(self.excel)

        self.btn_auto.clicked.connect(self.worker_auto)

        # self.btn_stop.clicked.connect(self.stop)

        self.worker = Worker()
        self.worker.sign_progress.connect(self.progress)
        self.worker.sign_done.connect(self.done)
        self.worker.sign_err.connect(self.err)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.tm = 0
        self.timer.timeout.connect(self._time)

        self.timer_auto = QTimer()
        self.timer_auto.setInterval(10 * 1000)
        self.timer_auto.timeout.connect(self.auto)

        self.settings = QSettings("db_config.ini", QSettings.IniFormat)
        try:
            self.conn = pymysql.connect(
                host=self.settings.value('DB/host'),
                user=self.settings.value('DB/user'),
                password=self.settings.value('DB/password'),
                db=self.settings.value('DB/db'),
                port=int(self.settings.value('DB/port')),
                charset='tis620',
                client_flag=CLIENT.MULTI_STATEMENTS,
                autocommit=False, )

            self.cur = self.conn.cursor()

            self.cur.execute(read('./sql_create.sql'))
            self.conn.commit()

            self.cur.execute("select distinct moo from plk_moph_id_person_check order by moo asc")
            data = self.cur.fetchall()
            for d in data:
                self.comboBox.addItem(d[0])
            self.comboBox.addItem('All')
        except Exception as e:
            self.txt_log.append(str(e))

    def stop(self):
        if self.worker.isRunning():
            print('Stopping Thread.')
            self.timer.stop()
            self.worker.stop()

    def err(self, data):
        self.txt_log.append(str(data))

    def excel(self):
        moo = self.comboBox.currentText().strip()
        sql = f"SELECT t.person_id,t.cid,t.pname,t.fname,t.lname,t.age_y,concat(\" \",t.address) address,t.moo,t.moph_id_check_result from plk_moph_id_person_check t where moo = '{moo}'"

        self.cur.execute(sql)
        data = self.cur.fetchall()
        file = f'data_{moo}.csv'
        with open(file, 'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['pid', 'cid', 'pname', 'fname', 'lname', 'age', 'address', 'moo', 'check_result'])
            for p in data:
                writer.writerow(p)
        os.startfile(file)

    def _time(self):
        self.tm = self.tm + 1
        sec = self.tm
        if sec < 60:
            self.lb_time.setText(f"ใช้เวลา {sec} วินาที")
        else:
            m = int(sec / 60)
            s = sec % 60
            self.lb_time.setText(f"ใช้เวลา {m} นาที {s} วินาที")

    def progress(self, data):
        print(data)
        self.txt_log.append(
            f"{data['i']}/{data['n']},{data['cid']} , {data['resp']['result']} , {data['resp']['RequestTime']} , ms : {data['resp']['processing_time_ms']}")

        p = (data['i'] * 100) / data['n']
        p = int(p)
        self.progressBar.setValue(p)
        self.lb_amount.setText(f"{data['i']} จาก {data['n']}")

    def db_config(self):
        os.startfile('db_config.ini')

    def token(self):
        os.startfile('token.txt')

    def done(self):
        self.timer.stop()

    def worker_begin(self):
        self.stop()
        self.timer_auto.stop()
        print('Begin.........................')
        self.txt_log.clear()
        self.timer.start()
        self.tm = 0
        self.worker.moo = self.comboBox.currentText().strip()
        self.worker.start()

    def worker_auto(self):
        print('Auto Click')
        self.timer_auto.stop()
        self.timer_auto.start()

    def auto(self):
        self.stop()
        print('Auto.........................')
        self.txt_log.clear()
        self.timer.start()
        self.tm = 0
        self.worker.moo = self.comboBox.currentText().strip()
        self.worker.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.excepthook = my_excepthook
    sys.exit(app.exec_())
