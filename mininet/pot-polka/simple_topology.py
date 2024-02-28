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

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.bmv2 import P4Switch

n_switches = 1
BW = 10


def topology(remote_controller=False):
    "Create a network."
    net = Mininet_wifi()

    # linkopts = dict()
    switches = {"1": None, "2": None, "3": None}

    # Source Host
    h1 = net.addHost(
        "h1", ip="10.0.1.1", mac="00:00:00:00:01:01")

    # Destination Host
    h2 = net.addHost(
        "h2", ip="10.0.2.2", mac="00:00:00:00:02:02")

    info("*** Adding P4Switches (core)\n")

    path = os.path.dirname(os.path.abspath(__file__))

    for i in switches:
        # read the network configuration
        json_file = f"{path}/pot-polka/pot-polka-s{i}.json"
        config = f"{path}/pot-polka/config/s{i}-commands.txt"
        # Add P4 switches (core)
        switch = net.addSwitch(
            f"s{i}",
            netcfg=True,
            json=json_file,
            thriftport=50000 + int(i),
            switch_config=config,
            loglevel="debug",
            cls=P4Switch,
        )
        switches[i] = switch

    info("*** Adding P4Switches (edge)\n")
    # read the network configuration
    # path = os.path.dirname(os.path.abspath(__file__))
    # json_file = path + "/pot-polka/pot-polka-edge.json"
    # config = path + "/pot-polka/config/e{}-commands.txt".format(1)
    # # add P4 switches (core)
    # src_edge = net.addSwitch(
    #     "e{}".format(1),
    #     netcfg=True,
    #     json=json_file,
    #     thriftport=50100 + int(1),
    #     switch_config=config,
    #     loglevel='debug',
    #     cls=P4Switch,
    # )

    # config = path + "/pot-polka/config/e{}-commands.txt".format(2)
    # # add P4 switches (core)
    # dst_edge = net.addSwitch(
    #     "e{}".format(2),
    #     netcfg=True,
    #     json=json_file,
    #     thriftport=50100 + int(2),
    #     switch_config=config,
    #     loglevel='debug',
    #     cls=P4Switch,
    # )

    info("*** Creating links\n")
    net.addLink(h1, switches["1"], bw=BW)
    net.addLink(h2, switches["3"], bw=BW)

    net.addLink(switches["1"], switches["2"], bw=BW)
    net.addLink(switches["2"], switches["3"], bw=BW)

    info("\n*** Starting network\n")
    net.start()
    net.staticArp()

    # disabling offload for rx and tx on each host interface

    h1.cmd(f"ethtool --offload {h1.name}-eth0 rx off tx off")
    h2.cmd(f"ethtool --offload {h2.name}-eth0 rx off tx off")

    info("*** Running CLI\n")
    CLI(net)

    os.system("pkill -9 -f 'xterm'")

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    topology()
