import os
import ctypes
from PyQt5.QtCore import *
import gui.gui_main as guim
import model.probe_dnn.probe as probe


dll_path = os.path.dirname(os.path.realpath(__file__)) + "/DLL20220722.dll"

# nsl-kdd dll 불러오기
nslkdd = ctypes.cdll.LoadLibrary(dll_path)
# 데이터 변환 결과값 형식 지정
nslkdd.rt_output.restype = ctypes.c_char_p


class DataReceiver(QThread):

    text_changed = pyqtSignal(str)
    count_changed = pyqtSignal(str)
    probe_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.count = 0
        self.probe = 0

    def run(self):
        # print("nsl-kdd data receiver start")
        self.text_changed.emit("nsl-kdd data receiver start")
        while True:
            if nslkdd.output_status():
                self.count += 1
                result = nslkdd.rt_output().decode("utf-8")
                # print(f"{result}")
                # guim.myWindow.kddTotalCount(self.count)
                self.count_changed.emit(str(self.count))

                # guim.myWindow.logAppend(result)
                # self.text_changed.emit(result)
                result_list = result.split(",")
                pmr = probe.probe_model(result_list)
                if pmr:
                    self.probe += 1
                    self.probe_changed.emit(str(self.probe))
                else:
                    self.text_changed.emit(str(probe.probe_model(result.split(","))))

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
