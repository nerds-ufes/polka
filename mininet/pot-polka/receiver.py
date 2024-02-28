#!/usr/bin/env python
import sys
from scapy.all import sniff, bind_layers
from scapy.all import Packet
from scapy.all import Ether
from scapy.fields import BitField


class SourceRoute(Packet):
    fields_desc = [
        BitField("routeid", 0, 160),
        BitField("rnd", 0, 16),
        BitField("cml", 0, 16)
    ]


bind_layers(Ether, SourceRoute, type=0x1234)


def handle_pkt(pkt):
    print("Got a packet!")
    pkt.show2()
    sys.stdout.flush()


def main():
    iface = sys.argv[1]

    print(f"Sniffing on {iface}")
    sys.stdout.flush()
    sniff(iface=iface, prn=lambda x: handle_pkt(x))


if __name__ == "__main__":
    main()
