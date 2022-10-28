from scapy.all import *


class Myiface:
    # 네트워크 인터페이스 선택
    def __init__(self):
        self.ifp = InterfaceProvider()

    def setIface(self, index):
        self.my_iface_index = index

        # 네트워크 인터페이스 디바이스 이름
        self.my_iface_dev = str(dev_from_index(self.my_iface_index))

        # 네트워크 인터페이스 이름
        self.my_iface = self.ifp._format(dev_from_index(self.my_iface_index))[1]

    def getIfaceDev(self):
        # 네트워크 디바이스 이름 반환
        return self.my_iface_dev

    def getIfaceName(self):
        # 네트워크 이름 반환
        return self.my_iface

    def showIfaceList(self):
        # 현재 시스템의 네트워크 인터페이스 리스트 반환
        return IFACES.show(print_result=False)
