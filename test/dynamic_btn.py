import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QApplication, QPushButton)

from PyQt5 import QtCore


class MainWindow(QMainWindow):
    def __init__(self):  # x <-- 3
        super().__init__()

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.lay = QVBoxLayout(self.centralwidget)
        for i in range(5):
            self.btn = QPushButton(f'Button {i + 1}', self)
            self.btn.clicked.connect(lambda checked, n=i + 1: self.handle_play_button(n))
            self.lay.addWidget(self.btn)

    def handle_play_button(self, n):
        print(n, self.sender().text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()  # 3 --> x
    mainWin.show()
    sys.exit(app.exec_())
