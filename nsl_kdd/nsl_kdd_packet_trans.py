import os
import ctypes
from PyQt5.QtCore import *

import model.probe_dnn.probe as probe
import model.dos_dnn.dos as dos
import datetime


# nsl-kdd dll 불러오기
dll_path = os.path.dirname(os.path.realpath(__file__)) + "/DLL20220722.dll"
nslkdd = ctypes.cdll.LoadLibrary(dll_path)

# 데이터 변환 결과값 형식 지정
nslkdd.rt_output.restype = ctypes.c_char_p


class DataReceiver(QThread):
    # nsl-kdd 데이터 받기
    text_changed = pyqtSignal(str)
    count_changed = pyqtSignal(str)
    probe_changed = pyqtSignal(str)
    dos_changed = pyqtSignal(str)
    ip_log = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.count = 0
        self.probe = 0
        self.dos = 0

    def run(self):
        self.text_changed.emit("[알림] nsl-kdd data receiver start")
        while True:
            if nslkdd.output_status():
                self.count += 1
                result = nslkdd.rt_output().decode("utf-8")

                result_list = result.split(",")

                # 값 변환 에러 방지
                for i in range(0, 28):
                    if i == 0 or i > 3:
                        if "0.00\\x" in result_list[i]:
                            result_list[i] = 0.00
                        result_list[i] = float(result_list[i])

                kdd_pkt_info = f"{result_list[-5]}:{result_list[-4]} -> {result_list[-3]}:{result_list[-2]}"
                time_now = datetime.datetime.now()

                ##########################################
                # 모델 판정
                pmr = probe.probe_model(result_list[:-5])
                if pmr:
                    self.probe += 1
                    self.text_changed.emit(
                        f"[공격 탐지됨] {time_now} - Probe ({kdd_pkt_info})"
                    )

                dmr = dos.dos_model(result_list[:-5])
                if dmr:
                    self.dos += 1
                    self.text_changed.emit(
                        f"[공격 탐지됨] {time_now} - DoS ({kdd_pkt_info})"
                    )

                # 수치 gui 반영
                self.count_changed.emit(str(self.count))
                self.probe_changed.emit(str(self.probe))
                self.dos_changed.emit(str(self.dos))

                nslkdd.output_false()


class PacketCapture(QThread):
    # nsl-kdd용 패킷 캡쳐
    text_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.text_changed.emit("[알림] nsl-kdd packet capture start")
        nslkdd.Test(self.dev_name)

    def setDevName(self, dev_name):
        self.dev_name = ctypes.c_char_p(dev_name.encode("utf-8"))
