#!/usr/bin/python
# Copyright [2019-2022] Universidade Federal do Espirito Santo
#                       Instituto Federal do Espirito Santo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.bmv2 import P4Switch

n_switches = 4
n_edge = 2
BW = 10


def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    # linkopts = dict()
    switches = []
    edges = []
    hosts = []

    info("*** Adding hosts\n")
    for i in range(1, 3):
        ip = "10.0.%d.%d" % (i, i)
        mac = "00:00:00:00:%02x:%02x" % (i, i)
        host = net.addHost("h%d" % i, ip=ip, mac=mac)
        hosts.append(host)

    info("*** Adding P4Switches (core)\n")
    for i in range(1, n_switches + 1):
        # read the network configuration
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = path + "/pot-polka/pot-polka-core.json"
        config = path + "/pot-polka/config/s{}-commands.txt".format(i)
        # Add P4 switches (core)
        switch = net.addSwitch(
            "s{}".format(i),
            netcfg=True,
            json=json_file,
            thriftport=50000 + int(i),
            switch_config=config,
            loglevel="info",
            cls=P4Switch,
        )
        switches.append(switch)

    info("*** Adding P4Switches (edge)\n")
    for i in range(1, n_edge + 1):
        # read the network configuration
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = path + "/pot-polka/pot-polka-edge.json"
        config = path + "/pot-polka/config/e{}-commands.txt".format(i)
        # add P4 switches (core)
        edge = net.addSwitch(
            "e{}".format(i),
            netcfg=True,
            json=json_file,
            thriftport=50100 + int(i),
            switch_config=config,
            loglevel="info",
            cls=P4Switch,
        )
        edges.append(edge)

    info("*** Creating links\n")

    net.addLink(hosts[0], edges[0], bw=BW)
    net.addLink(hosts[1], edges[1], bw=BW)
    net.addLink(edges[0], switches[0], bw=BW)
    net.addLink(edges[1], switches[3], bw=BW)

    # net.addLink(hosts[2], edges[1], bw=BW)
    #1Path
    net.addLink(switches[0], switches[1], bw=BW)
    net.addLink(switches[1], switches[2], bw=BW)
    net.addLink(switches[2], switches[3], bw=BW)

    info("*** Starting network\n")
    net.start()
    net.staticArp()

    # # disabling offload for rx and tx on each host interface
    for host in hosts:
        host.cmd(f"ethtool --offload {host.name}-eth0 rx off tx off")
        host.cmd(f"ifconfig {host.name}-eth0 mtu 1500")



    info("*** Running CLI\n")
    CLI(net)

    os.system("pkill -9 -f 'xterm'")

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)