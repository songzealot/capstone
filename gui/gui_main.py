import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import nsl_kdd.nsl_kdd_packet_trans as nslkdd
import cic.sniffer as cic
from . import iface

from . import iface_select
from . import team

# UI파일 연결
ui_path = os.path.dirname(os.path.realpath(__file__)) + "/main.ui"

form_class = uic.loadUiType(ui_path)[0]

# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1280, 720)

        self.kdd_tot = 0
        self.kdd_dos_w = 0
        self.kdd_prb_w = 0
        self.cic_tot = 0
        self.cic_bf_w = 0
        self.cic_ddos_w = 0

        self.ifacefunc = iface.Myiface()
        # print(self.ifacefunc.showIfaceList())
        self.ifacelist_sliced = self.ifacefunc.showIfaceList().split("\n")
        del self.ifacelist_sliced[0]

        self.ifaceWindow(self.ifacelist_sliced)

        # self.ifacefunc.setIface(input("네트워크 Index 번호를 입력\n"))
        self.ifacefunc.setIface(self.iface_selected)
        iface_name = self.ifacefunc.getIfaceName()
        print(f"{iface_name} 선택됨")
        self.selected_network.setText(str(iface_name))

        # 패킷 카운트
        self.pckt_log = cic.PcktLog(iface_name)
        self.pckt_log.ip_count.connect(self.captured_packets.setText)
        self.pckt_log.ip_log.connect(self.ip_log_box.append)
        self.pckt_log.start_log.connect(self.log_box.append)

        # nslkdd, cic 패킷 캡쳐-데이터 특징 생성 스레드
        self.dr_th = nslkdd.DataReceiver()
        self.pkc_th = nslkdd.PacketCapture()
        self.cic_th = cic.CicTest()

        # nslkdd, cic 스레드의 네트워크 인터페이스 설정
        self.pkc_th.setDevName(self.ifacefunc.getIfaceDev())
        self.cic_th.setIface(self.ifacefunc.getIfaceName())

        # 로그박스 출력(임시)
        self.cicstr = CicStr()
        self.cicstr.cic_result.connect(self.log_box.append)
        self.cic_th.text_changed.connect(self.log_box.append)
        self.dr_th.text_changed.connect(self.log_box.append)
        self.pkc_th.text_changed.connect(self.log_box.append)
        # self.cicstr.cic_ip_log.connect(self.ip_log_box.append)
        # self.dr_th.ip_log.connect(self.ip_log_box.append)

        # kdd 수치 변경
        self.dr_th.count_changed.connect(self.kdd_data_total.setText)
        self.dr_th.count_changed.connect(self.kddTotalCount)
        self.dr_th.probe_changed.connect(self.kdd_probe_warning.setText)
        self.dr_th.dos_changed.connect(self.kdd_dos_warning.setText)

        # cic 수치 변경
        self.cicstr.cic_count.connect(self.cic_data_total.setText)
        self.cicstr.cic_bf_count.connect(self.cic_bf_warning.setText)
        self.cicstr.cic_ddos_count.connect(self.cic_ddos_warning.setText)

        #############################################################################
        #############################################################################
        # 기본 그래프 정보
        self.colors = ["red", "green"]
        self.labels = ["attack", "normal"]

        # DoS 그래프
        self.fig_dos, self.ax_dos = plt.subplots()
        self.canvas_dos = FigureCanvasQTAgg(self.fig_dos)

        self.graph_layout.addWidget(self.canvas_dos)
        self.ani_dos = animation.FuncAnimation(
            self.fig_dos,
            self.update_dos,
            interval=100,
            blit=False,
            save_count=50,
        )
        self.canvas_dos.draw()

        # Probe 그래프
        self.fig_prb, self.ax_prb = plt.subplots()
        self.canvas_prb = FigureCanvasQTAgg(self.fig_prb)

        self.graph_layout.addWidget(self.canvas_prb)
        self.ani_prb = animation.FuncAnimation(
            self.fig_prb,
            self.update_prb,
            interval=100,
            blit=False,
            save_count=50,
        )
        self.canvas_prb.draw()

        # Brute Foce 그래프
        self.fig_bf, self.ax_bf = plt.subplots()
        self.canvas_bf = FigureCanvasQTAgg(self.fig_bf)

        self.graph_layout.addWidget(self.canvas_bf)
        self.ani_bf = animation.FuncAnimation(
            self.fig_bf,
            self.update_bf,
            interval=100,
            blit=False,
            save_count=50,
        )
        self.canvas_bf.draw()

        # DDoS 그래프
        self.fig_ddos, self.ax_ddos = plt.subplots()
        self.canvas_ddos = FigureCanvasQTAgg(self.fig_ddos)

        self.graph_layout.addWidget(self.canvas_ddos)
        self.ani_ddos = animation.FuncAnimation(
            self.fig_ddos,
            self.update_ddos,
            interval=100,
            blit=False,
            save_count=50,
        )
        self.canvas_ddos.draw()

        self.show()

        # 기타 gui
        self.action.setShortcut("Ctrl+I")
        self.action.triggered.connect(self.teamWindow)
        self.action_2.setShortcut("Ctrl+Q")
        self.action_2.triggered.connect(qApp.quit)

    def update_dos(self, frame):
        self.ax_dos.clear()
        self.ax_dos.axis("equal")
        nums = ["", ""]

        a = int(self.kdd_dos_warning.text())
        b = int(self.kdd_data_total.text()) - a
        if a == 0 and b == 0:
            b = 1
        nums[0] = a
        nums[1] = b

        self.ax_dos.pie(
            nums,
            labels=self.labels,
            colors=self.colors,
            autopct="%1.1f%%",
            startangle=90,
        )
        self.ax_dos.set_title("DoS")

    def update_prb(self, frame):
        self.ax_prb.clear()
        self.ax_prb.axis("equal")
        nums = ["", ""]

        a = int(self.kdd_probe_warning.text())
        b = int(self.kdd_data_total.text()) - a
        if a == 0 and b == 0:
            b = 1
        nums[0] = a
        nums[1] = b

        self.ax_prb.pie(
            nums,
            labels=self.labels,
            colors=self.colors,
            autopct="%1.1f%%",
            startangle=90,
        )
        self.ax_prb.set_title("Probe")

    def update_bf(self, frame):
        self.ax_bf.clear()
        self.ax_bf.axis("equal")
        nums = ["", ""]

        a = int(self.cic_bf_warning.text())
        b = int(self.cic_data_total.text()) - a
        if a == 0 and b == 0:
            b = 1
        nums[0] = a
        nums[1] = b

        self.ax_bf.pie(
            nums,
            labels=self.labels,
            colors=self.colors,
            autopct="%1.1f%%",
            startangle=90,
        )
        self.ax_bf.set_title("Brute Force")

    def update_ddos(self, frame):
        self.ax_ddos.clear()
        self.ax_ddos.axis("equal")
        nums = ["", ""]

        a = int(self.cic_ddos_warning.text())
        b = int(self.cic_data_total.text()) - a
        if a == 0 and b == 0:
            b = 1
        nums[0] = a
        nums[1] = b

        self.ax_ddos.pie(
            nums,
            labels=self.labels,
            colors=self.colors,
            autopct="%1.1f%%",
            startangle=90,
        )
        self.ax_ddos.set_title("DDoS")

    def threadStart(self):
        self.dr_th.start()
        self.pkc_th.start()
        self.cic_th.start()
        self.pckt_log.start()

    # def buttonStop(self):
    #     self.pkc_th.stop()
    #     self.dr_th.stop()
    #     self.cic_th.stop()

    # def packetCount(self, count):
    # 캡쳐된 패킷 gui 표시
    # self.captured_packets.setText(str(count))

    def kddTotalCount(self, count):
        # kdd 전체 변환 데이터 카운트(그래프용)
        # self.kdd_data_total.setText(str(count))
        self.kdd_tot = int(count)

    def cicTotalCount(self, count):
        # cic 전체 변환 데이터 카운트(그래프용)
        # self.cic_data_total.setText(str(count))
        self.cic_tot = int(count)

    def logAppend(self, log_data):
        # 로그 박스에 내용 추가
        self.log_box.append(str(log_data))
        self.log_box.verticalScrollBar().setValue(
            self.log_box.verticalScrollBar().maximum()
        )

    def ifaceWindow(self, iflist):
        # 인터페이스 선택 화면 출력
        ifwindow = iface_select.IfaceSelectGUI(iflist)
        ifwindow.exec_()
        self.iface_selected = ifwindow.iface_index
        # print(ifwindow.iface_index)

    def teamWindow(self):
        # 팀 소개 화면 출력
        team_about = team.TeamGUI()
        team_about.exec_()


class CicStr(QObject):
    # cic 데이터 gui 표시
    cic_result = pyqtSignal(str)
    cic_count = pyqtSignal(str)
    cic_bf_count = pyqtSignal(str)
    cic_ddos_count = pyqtSignal(str)
    cic_ip_log = pyqtSignal(str)

    def setResult(self, result):
        # 공격 탐지 로그 표시
        self.cic_result.emit(result)

    def setTotalCount(self, count):
        # cic 전체 변환 데이터 gui 표시
        self.cic_count.emit(str(count))

    def setBFCount(self, count):
        self.cic_bf_count.emit(str(count))

    def setDDoSCount(self, count):
        self.cic_ddos_count.emit(str(count))

    def ipLog(self, ip_info):
        self.cic_ip_log.emit(str(ip_info))


app = QApplication(sys.argv)
myWindow = WindowClass()
myWindow.threadStart()


def createdGuiShow():
    myWindow.show()


def pyqtAppExec():
    app.exec_()
