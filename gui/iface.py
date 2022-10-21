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
        return self.my_iface_dev

    def getIfaceName(self):
        return self.my_iface

    def showIfaceList(self):
        return IFACES.show(print_result=False)
