import os
import sys
import time

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QMessageBox, \
    QFileDialog, QDialog
from PyQt5.QtCore import QThread, QTimer, QEventLoop, pyqtSignal, QSettings, QObject
from PyQt5.QtGui import QIcon

from PyQt5 import uic, QtCore


def my_excepthook(type, value, tback):
    print(type, value, tback)
    sys.__excepthook__(type, value, tback)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('test_thread.ui', self)

        self.progressBar_1.setValue(0)
        self.progressBar_2.setValue(0)

        self.thread = dict()
        self.thread[1] = ThreadClass(index=1)
        self.thread[2] = ThreadClass(index=2)

        print(self.thread)

        self.btn_t_1.clicked.connect(lambda: self.do_click(1))
        self.btn_t_1.setText('Click')

        self.btn_t_2.clicked.connect(lambda: self.do_click(2))
        self.btn_t_2.setText('Click')

    def do_click(self, index):
        if self.thread[index].is_running:
            self.thread[index].stop()

        else:
            self.thread[index].signal.connect(self.my_progress)
            self.thread[index].start()

    def my_progress(self, cnt):
        index = self.sender().index
        if index == 1:
            self.progressBar_1.setValue(cnt)
        if index == 2:
            self.progressBar_2.setValue(cnt)


class ThreadClass(QThread):
    signal = pyqtSignal(int)

    def __init__(self, index=0):
        super(ThreadClass, self).__init__()
        self.index = index
        self.p = 0
        self.is_running = False

    def run(self):
        self.is_running = True
        while True:
            self.p += 1
            if self.p == 99: self.p = 0
            time.sleep(0.1)
            self.signal.emit(self.p)

    def stop(self):
        self.is_running = False
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.excepthook = my_excepthook
    sys.exit(app.exec_())
