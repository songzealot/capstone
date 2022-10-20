import os
import ctypes
from PyQt5.QtCore import *

import model.probe_dnn.probe as probe
import model.dos_dnn.dos as dos
import datetime


dll_path = os.path.dirname(os.path.realpath(__file__)) + "/DLL20220722.dll"

# nsl-kdd dll 불러오기
nslkdd = ctypes.cdll.LoadLibrary(dll_path)
# 데이터 변환 결과값 형식 지정
nslkdd.rt_output.restype = ctypes.c_char_p


class DataReceiver(QThread):

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
        # print("nsl-kdd data receiver start")
        self.text_changed.emit("nsl-kdd data receiver start")
        while True:
            if nslkdd.output_status():
                self.count += 1
                result = nslkdd.rt_output().decode("utf-8")
                # print(result)
                # print(f"{result}")
                # guim.myWindow.kddTotalCount(self.count)
                self.count_changed.emit(str(self.count))

                # guim.myWindow.logAppend(result)
                # self.text_changed.emit(result)
                result_list = result.split(",")
                # print(result_list)
                # for i in range(0, 28):
                #     if i == 0 or (4 <= i and i < 11):
                #         result_list[i] = int(result_list[i])
                #     elif 11 <= i:
                #         result_list[i] = float(result_list[i])
                for i in range(0, 28):
                    if i == 0 or i > 3:
                        if "0.00\\x" in result_list[i]:
                            result_list[i] = 0.00
                        result_list[i] = float(result_list[i])
                # print(result_list[:-5])
                # print(result_list[-5:])
                kdd_pkt_info = f"{result_list[-5]}:{result_list[-4]} -> {result_list[-3]}:{result_list[-2]}"
                #
                time_now = datetime.datetime.now()

                self.ip_log.emit(str(f"{str(result_list[1]).upper()}\t{kdd_pkt_info}"))

                ##########################################
                pmr = probe.probe_model(result_list[:-5])
                if pmr:
                    self.probe += 1
                    self.probe_changed.emit(str(self.probe))
                    self.text_changed.emit(
                        f"[공격 탐지됨] {time_now} - Probe ({kdd_pkt_info})"
                    )
                # else:
                # self.text_changed.emit(str(probe.probe_model(result.split(","))))
                # self.text_changed.emit("Probe: " + str(pmr))

                dmr = dos.dos_model(result_list[:-5])
                if dmr:
                    self.dos += 1
                    self.dos_changed.emit(str(self.dos))
                    self.text_changed.emit(
                        f"[공격 탐지됨] {time_now} - DoS ({kdd_pkt_info})"
                    )
                # else:
                # self.text_changed.emit(str(probe.probe_model(result.split(","))))
                # self.text_changed.emit("DoS: " + str(dmr))
                ##########################################

                nslkdd.output_false()

                # 모델 적용 부분
                # 모델이 아직 없음

    def stop(self):
        self.quit()
        self.text_changed.emit("nsl-kdd data receiver stop")


class PacketCapture(QThread):
    text_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.text_changed.emit("nsl-kdd packet capture start")
        # print("nsl-kdd packet capture start")
        nslkdd.Test(self.dev_name)

    def stop(self):
        self.quit()
        self.text_changed.emit("nsl-kdd packet capture stop")

    def setDevName(self, dev_name):
        self.dev_name = ctypes.c_char_p(dev_name.encode("utf-8"))
