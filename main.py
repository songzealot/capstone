import cic.sniffer as cic
from scapy.all import *
import nsl_kdd.nsl_kdd_packet_trans as nslkdd
import gui.gui_main as gui

IFACES.show()
my_iface_index = input("네트워크 Index 번호를 입력\n")
ifp = InterfaceProvider()

# 네트워크 인터페이스 디바이스 이름
my_iface_name = str(dev_from_index(my_iface_index))

# 네트워크 인터페이스 이름
my_iface = ifp._format(dev_from_index(my_iface_index))[1]
print(f"{my_iface} 선택됨")
# csv_name = input("저장할 csv 파일 이름\n")
# csv_name += ".csv"

# nsl-kdd 데이터 변환 스레드 시작
dr_th = nslkdd.DataReceiver()
pkc_th = nslkdd.PacketCapture(my_iface_name)
dr_th.start()
pkc_th.start()

# cic 데이터 변환 스레드 시작
test_sniffer = cic.create_sniffer(None, my_iface, "flow", None)
test_sniffer.start()
# test_sniffer.join()

gui.myWindow.show()
gui.app.exec_()


# 스레드 동작 중 에러 발생 -> qthread로 변환 필요


# try:
#     test_sniffer.join()
# except KeyboardInterrupt:
#     test_sniffer.stop()
# finally:
#     # test_sniffer.join()
#     print("종료")
