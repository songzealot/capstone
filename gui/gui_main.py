import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import os

import nsl_kdd.nsl_kdd_packet_trans as nslkdd
import cic.sniffer as cic
from . import iface

# import main as mmm

# UI파일 연결
ui_path = os.path.dirname(os.path.realpath(__file__)) + "/main.ui"

form_class = uic.loadUiType(ui_path)[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ifacefunc = iface.Myiface()
        print(self.ifacefunc.showIfaceList())
        self.ifacefunc.setIface(input("네트워크 Index 번호를 입력\n"))
        print(f"{self.ifacefunc.getIfaceName()} 선택됨")

        # nslkdd, cic 패킷 캡쳐-데이터 특징 생성 스레드
        self.dr_th = nslkdd.DataReceiver()
        self.pkc_th = nslkdd.PacketCapture()
        self.cic_th = cic.cicTest()

        # nslkdd, cic 스레드의 네트워크 인터페이스 설정
        self.pkc_th.setDevName(self.ifacefunc.getIfaceDev())
        self.cic_th.setIface(self.ifacefunc.getIfaceName())

        # 버튼
        self.button_start.clicked.connect(self.buttonStart)

        # 로그박스 출력(임시)
        self.cicstr = CicStr()
        self.cicstr.cic_result.connect(self.log_box.append)
        self.cic_th.text_changed.connect(self.log_box.append)
        self.dr_th.text_changed.connect(self.log_box.append)
        self.pkc_th.text_changed.connect(self.log_box.append)

    def buttonStart(self):

        # self.captured_packets.setText("테스트")

        self.dr_th.start()
        self.pkc_th.start()
        self.cic_th.start()

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


class CicStr(QObject):
    cic_result = pyqtSignal(str)

    def setResult(self, result):
        self.cic_result.emit(result)


app = QApplication(sys.argv)
myWindow = WindowClass()


def createdGuiShow():
    myWindow.show()


def pyqtAppExec():
    app.exec_()
