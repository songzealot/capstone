# vram 사전 할당 해제
import tensorflow as tf

gpu_devices = tf.config.experimental.list_physical_devices("GPU")
tf.config.experimental.set_memory_growth(gpu_devices[0], True)


# import cic.sniffer as cic

# from scapy.all import *
# import nsl_kdd.nsl_kdd_packet_trans as nslkdd
import gui.gui_main as guim


# import gui.iface as iface

# IFACES.show()

# my_iface_index = input("네트워크 Index 번호를 입력\n")

# ifp = InterfaceProvider()


# csv_name = input("저장할 csv 파일 이름\n")
# csv_name += ".csv"


# 클래스 정의만 되어있는 상태에서 메소드 호출
# iface값 따로 넘기기 수정 필요
# nslkdd.PacketCapture.setDevName(my_iface_name)
# cic.cicTest.setIface(my_iface)


# nsl-kdd 데이터 변환 스레드 시작
# dr_th = nslkdd.DataReceiver()
# pkc_th = nslkdd.PacketCapture(my_iface_name)
# dr_th.start()
# pkc_th.start()

# cic 데이터 변환 스레드 시작
# test_sniffer = cic.create_sniffer(None, my_iface, "flow", None)
# test_sniffer.start()
# test_sniffer.join()

guim.createdGuiShow()
guim.pyqtAppExec()


# 스레드 동작 중 에러 발생 -> qthread로 변환 필요


# try:
#     test_sniffer.join()
# except KeyboardInterrupt:
#     test_sniffer.stop()
# finally:
#     # test_sniffer.join()
#     print("종료")
