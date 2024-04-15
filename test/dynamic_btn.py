import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QApplication, QPushButton)

from PyQt5 import QtCore


class MainWindow(QMainWindow):
    def __init__(self):  # x <-- 3
        super().__init__()

        deps = [{'id': '001', 'name': 'OPD'}, {'id': '002', 'name': 'ศัลยกรรม'}]

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.lay = QVBoxLayout(self.centralwidget)
        for dep in deps:
            self.btn = QPushButton(dep['name'], self)
            self.btn.clicked.connect(
                lambda n,code=dep['id'], name=dep['name']: self.handle_play_button(code, name))
            self.lay.addWidget(self.btn)
            self.lay.addStretch(1)

    def handle_play_button(self, code, name):
        print(code, name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()  # 3 --> x
    mainWin.show()
    sys.exit(app.exec_())
