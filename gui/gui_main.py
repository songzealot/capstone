import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

# UI파일 연결
ui_path = os.path.dirname(os.path.realpath(__file__)) + "/main.ui"

form_class = uic.loadUiType(ui_path)[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button_start.clicked.connect(self.buttonStart)

    def buttonStart(self):
        self.captured_packets.setText("테스트")

    def packetCount(self, count):
        self.captured_packets.setText(str(count))

    def kddTotalCount(self, count):
        self.kdd_data_total.setText(str(count))

    def cicTotalCount(self, count):
        self.cic_data_total.setText(str(count))

    def logAppend(self, log_data):
        self.log_box.append(str(log_data))
        self.log_box.verticalScrollBar().setValue(
            self.log_box.verticalScrollBar().maximum()
        )


app = QApplication(sys.argv)

myWindow = WindowClass()
