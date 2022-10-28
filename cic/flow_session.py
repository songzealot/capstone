from collections import defaultdict

from scapy.sessions import DefaultSession

from .features.context.packet_direction import PacketDirection
from .features.context.packet_flow_key import get_packet_flow_key
from .flow import Flow

from model.bruteforce_cic import bf
from model.ddos_cic import ddos

import gui.gui_main as guim
from PyQt5.QtCore import *
import datetime

EXPIRED_UPDATE = 40
MACHINE_LEARNING_API = "http://localhost:8000/predict"
GARBAGE_COLLECT_PACKETS = 100


#################################
# 라이브러리 원본에서 일부 수정됨 #
#################################


class FlowSession(DefaultSession):

    """Creates a list of network flows."""

    def __init__(self, *args, **kwargs):
        self.flows = {}
        self.csv_line = 0
        self.bf_attack_count = 0
        self.ddos_attack_count = 0

        self.packets_count = 0

        self.clumped_flows_per_label = defaultdict(list)

        super(FlowSession, self).__init__(*args, **kwargs)

    def toPacketList(self):
        # Sniffer finished all the packets it needed to sniff.
        # It is not a good place for this, we need to somehow define a finish signal for AsyncSniffer
        self.garbage_collect(None)
        return super(FlowSession, self).toPacketList()

    def on_packet_received(self, packet):
        count = 0
        direction = PacketDirection.FORWARD

        if self.output_mode != "flow":
            if "TCP" not in packet:
                return
            elif "UDP" not in packet:
                return

        try:
            # Creates a key variable to check
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))
        except Exception:
            return

        # If there is no forward flow with a count of 0
        if flow is None:
            # There might be one of it in reverse
            direction = PacketDirection.REVERSE
            packet_flow_key = get_packet_flow_key(packet, direction)
            flow = self.flows.get((packet_flow_key, count))

        if flow is None:
            # If no flow exists create a new flow
            direction = PacketDirection.FORWARD
            flow = Flow(packet, direction)
            packet_flow_key = get_packet_flow_key(packet, direction)
            self.flows[(packet_flow_key, count)] = flow

        elif (packet.time - flow.latest_timestamp) > EXPIRED_UPDATE:
            # If the packet exists in the flow but the packet is sent
            # after too much of a delay than it is a part of a new flow.
            expired = EXPIRED_UPDATE
            while (packet.time - flow.latest_timestamp) > expired:
                count += 1
                expired += EXPIRED_UPDATE
                flow = self.flows.get((packet_flow_key, count))

                if flow is None:
                    flow = Flow(packet, direction)
                    self.flows[(packet_flow_key, count)] = flow
                    break
        elif "F" in str(packet.flags):
            # 분기 1
            # If it has FIN flag then early collect flow and continue
            flow.add_packet(packet, direction)
            self.garbage_collect(packet.time)
            return

        flow.add_packet(packet, direction)

        if not self.url_model:
            GARBAGE_COLLECT_PACKETS = 10000

        if self.packets_count % GARBAGE_COLLECT_PACKETS == 0 or (
            flow.duration > 120 and self.output_mode == "flow"
        ):
            # 분기 2
            self.garbage_collect(packet.time)

    def get_flows(self) -> list:
        return self.flows.values()

    def garbage_collect(self, latest_time) -> None:
        # TODO: Garbage Collection / Feature Extraction should have a separate thread
        # if not self.url_model:
        #     print("Garbage Collection Began. Flows = {}".format(len(self.flows)))
        keys = list(self.flows.keys())
        for k in keys:
            flow = self.flows.get(k)

            if (
                latest_time is None
                or latest_time - flow.latest_timestamp > EXPIRED_UPDATE
                or flow.duration > 90
            ):

                ########################################
                # 분석 결과
                data_ms = flow.get_ms_data()
                ms_list = list(data_ms.values())[5:]
                ms_result = bf.bruteForce(ms_list)

                data_jh = flow.get_jh_data()
                jh_list = list(data_jh.values())[5:]
                jh_result = ddos.ddos(jh_list)

                # gui 표시
                self.csv_line += 1
                guim.myWindow.cicstr.setTotalCount(self.csv_line)

                # ip 정보
                ms_pkt_info = list(data_ms.values())[:5]

                # gui 표시
                if ms_result == 1:
                    self.bf_attack_count += 1
                    guim.myWindow.cicstr.setBFCount(self.bf_attack_count)
                    guim.myWindow.cicstr.setResult(
                        f"[공격 탐지됨] {datetime.datetime.now()} - Brute Force ({ms_pkt_info[0]}:{ms_pkt_info[2]} -> {ms_pkt_info[1]}:{ms_pkt_info[3]})"
                    )

                if jh_result == 1:
                    self.ddos_attack_count += 1
                    guim.myWindow.cicstr.setDDoSCount(self.ddos_attack_count)
                    guim.myWindow.cicstr.setResult(
                        f"[공격 탐지됨] {datetime.datetime.now()} - DDoS ({ms_pkt_info[0]}:{ms_pkt_info[2]} -> {ms_pkt_info[1]}:{ms_pkt_info[3]})"
                    )

                del self.flows[k]


def generate_session_class(output_mode, url_model):
    return type(
        "NewFlowSession",
        (FlowSession,),
        {
            "output_mode": output_mode,
            # "output_file": output_file,
            "url_model": url_model,
        },
    )
