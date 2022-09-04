import os
import ctypes
import threading

dll_path = os.path.dirname(os.path.realpath(__file__)) + "/DLL20220722.dll"

# nsl-kdd dll 불러오기
nslkdd = ctypes.cdll.LoadLibrary(dll_path)
# 데이터 변환 결과값 형식 지정
nslkdd.rt_output.restype = ctypes.c_char_p


class DataReceiver(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        print("nsl-kdd data receiver start")
        while True:
            if nslkdd.output_status():
                print(f"{nslkdd.rt_output()}")
                nslkdd.output_false()


class PacketCapture(threading.Thread):
    def __init__(self, dev_name):
        super().__init__()
        self.dev_name = ctypes.c_char_p(dev_name.encode("utf-8"))

    def run(self):
        print("nsl-kdd packet capture start")
        nslkdd.Test(self.dev_name)
