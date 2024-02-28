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
BW = 10


def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    # linkopts = dict()
    switches = []
    edges = []

    # Source Host
    ip = "10.0.%d.%d" % (1, 1)
    mac = "00:00:00:00:%02x:%02x" % (1, 1)
    src_host = net.addHost("src_host", ip=ip, mac=mac)

    # Source Host
    ip = "10.0.%d.%d" % (1, 10)
    mac = "00:00:00:00:%02x:%02x" % (1, 10)
    dst_host = net.addHost("dst_host", ip=ip, mac=mac)

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
            loglevel='debug',
            cls=P4Switch,
        )
        switches.append(switch)

    info("*** Adding P4Switches (edge)\n")
    # read the network configuration
    path = os.path.dirname(os.path.abspath(__file__))
    json_file = path + "/pot-polka/pot-polka-edge.json"
    config = path + "/pot-polka/config/e{}-commands.txt".format(1)
    # add P4 switches (core)
    src_edge = net.addSwitch(
        "e{}".format(1),
        netcfg=True,
        json=json_file,
        thriftport=50100 + int(1),
        switch_config=config,
        loglevel='debug',
        cls=P4Switch,
    )

    config = path + "/pot-polka/config/e{}-commands.txt".format(2)
    # add P4 switches (core)
    dst_edge = net.addSwitch(
        "e{}".format(2),
        netcfg=True,
        json=json_file,
        thriftport=50100 + int(2),
        switch_config=config,
        loglevel='debug',
        cls=P4Switch,
    )

    info("*** Creating links\n")
    net.addLink(src_host, src_edge)
    net.addLink(dst_host, dst_edge)

    net.addLink(src_edge, switches[0], bw=BW)
    net.addLink(dst_edge, switches[2], bw=BW)
    net.addLink(switches[0], switches[1], bw=BW)
    net.addLink(switches[0], switches[3], bw=BW)
    net.addLink(switches[1], switches[2], bw=BW)
    net.addLink(switches[2], switches[3], bw=BW)

    info("*** Starting network\n")
    net.start()
    net.staticArp()

    # disabling offload for rx and tx on each host interface

    src_host.cmd("ethtool --offload {}-eth0 rx off tx off".format(src_host.name))
    dst_host.cmd("ethtool --offload {}-eth0 rx off tx off".format(dst_host.name))

    info("*** Running CLI\n")
    CLI(net)

    os.system("pkill -9 -f 'xterm'")

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
