import ctypes
import threading

# nsl-kdd dll 불러오기
nslkdd = ctypes.cdll.LoadLibrary("./DLL20220722.dll")
# 데이터 변환 결과값 형식 지정
nslkdd.rt_output.restype = ctypes.c_char_p


class DataReceiver(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        print("nsl-kdd data receiver start")
        while True:
            if nslkdd.output_status():
                print(f"반환된 데이터\n{nslkdd.rt_output()}")
                nslkdd.output_false()


class PacketCapture(threading.Thread):
    def __init__(self, dev_name):
        super().__init__()
        self.dev_name = dev_name

    def run(self):
        nslkdd.Test(self.dev_name)
