import cic.sniffer as cic
from scapy.all import *

IFACES.show()
my_iface_index = input("네트워크 Index 번호를 입력\n")
ifp = InterfaceProvider()

# 네트워크 인터페이스 디바이스 이름
my_iface_name = dev_from_index(my_iface_index)
print(my_iface_name)

# 네트워크 인터페이스 이름
my_iface = ifp._format(dev_from_index(my_iface_index))[1]
print(f"{my_iface} 선택됨")
# csv_name = input("저장할 csv 파일 이름\n")
# csv_name += ".csv"

# cic 데이터 변환 스레드 시작
test_sniffer = cic.create_sniffer(None, my_iface, "flow", None)
test_sniffer.start()

try:
    test_sniffer.join()
except KeyboardInterrupt:
    test_sniffer.stop()
finally:
    test_sniffer.join()
    print("종료")
