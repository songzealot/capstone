########################################################################
# 사용법
# 1. pip install scapy 로 scapy 설치
# 2. cic_packet_trans.py 실행
# 3. 왜인지는 몰라도 Ctrl + C로 안멈추므로 그냥 프로그램(터미널) 종료할 것
# 4. csv파일은 현재 터미널에 띄워진 경로 위치에 저장됨
#
#
# 기존 cic도 넣어는 놨는데 버그가 있어서 중간에 터짐
# csv에 내용 저장이 안되는 경우가 있는데 아직 해결 중
# csv 저장이 안될때 다시 시도하면 됨
#
# 파이썬 3.9.2 64비트 기준
########################################################################

import pack.sniffer
from scapy.all import *

IFACES.show()
my_iface_index = input("네트워크 Index 번호를 입력\n")
ifp = InterfaceProvider()
my_iface = ifp._format(dev_from_index(my_iface_index))[1]
print(f"{my_iface} 선택됨")
csv_name = input("저장할 csv 파일 이름\n")
csv_name += ".csv"
test_sniffer = pack.sniffer.create_sniffer(None, my_iface, "flow", csv_name, None)
test_sniffer.start()

try:
    test_sniffer.join()
except KeyboardInterrupt:
    test_sniffer.stop()
finally:
    test_sniffer.join()
    print("종료")
