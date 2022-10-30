from scapy.sendrecv import AsyncSniffer

from . import flow_session as fs
from PyQt5.QtCore import *

from scapy.all import *

#################################
# 라이브러리 원본에서 일부 수정됨 #
#################################


def create_sniffer(input_file, input_interface, output_mode, url_model=None):
    # cic 데이터 변환 시작
    assert (input_file is None) ^ (input_interface is None)

    NewFlowSession = fs.generate_session_class(output_mode, url_model)

    if input_file is not None:
        return AsyncSniffer(
            offline=input_file,
            filter="ip and (tcp or udp)",
            prn=None,
            session=NewFlowSession,
            store=False,
        )
    else:
        return AsyncSniffer(
            iface=input_interface,
            filter="ip and (tcp or udp)",
            prn=None,
            session=NewFlowSession,
            store=False,
        )


class CicTest(QThread):
    # cic 데이터 변환 스레드
    text_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        self.text_changed.emit("[알림] cic packet converter start")
        self.sniffer = create_sniffer(None, self.my_iface, "flow", None)
        self.sniffer.start()

    def setIface(self, my_iface):
        self.my_iface = my_iface


class PcktLog(QThread):
    # 패킷 카운트, 로그 기록
    ip_count = pyqtSignal(str)
    ip_log = pyqtSignal(str)
    start_log = pyqtSignal(str)
    protocols = {
        1: "ICMP",
        2: "IGMP",
        3: "GGP",
        4: "IPv4",
        5: "ST",
        6: "TCP",
        7: "CBT",
        8: "EGP",
        9: "IGP",
        17: "UDP",
    }
    count = 0

    def __init__(self, iface):
        super().__init__()
        self.iface = iface

    def run(self):
        self.start_log.emit("[알림] packet counter start")
        self.pcktSniff()

    def pcktInfo(self, pckt):
        # 패킷 정보 기록
        self.count += 1
        src_ip = pckt[0][1].src
        dst_ip = pckt[0][1].dst
        proto = pckt[0][1].proto

        if pckt[0][1].proto == 6 or pckt[0][1].proto == 17:
            src_port = pckt[0][2].sport
            dst_port = pckt[0][2].dport
            info = (
                f"{self.protocols[proto]}\t{src_ip}:{src_port} -> {dst_ip}:{dst_port}"
            )
        elif pckt[0][1].proto:
            info = f"{self.protocols[proto]}\t{src_ip} -> {dst_ip}"

        self.ip_count.emit(str(self.count))
        self.ip_log.emit(info)

    def pcktSniff(self):
        sniff(filter="ip", prn=self.pcktInfo, count=0, iface=self.iface)
