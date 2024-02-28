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
#from run_exp import run_latency_test, run_latency_test_bigpacket
#from run_exp import run_latency_test_background_traffic
#from run_exp import run_iperf_test, run_jitter_test
#from run_exp import run_fct_test
from time import sleep

n_switches = 10
BW = 10


def topology(remote_controller):
    "Create a network."
    net = Mininet_wifi()

    # linkopts = dict()
    switches = []
    edges = []
    hosts = []

    info("*** Adding hosts\n")
    for i in range(1, n_switches + 1):
        ip = "10.0.%d.%d" % (i, i)
        mac = "00:00:00:00:%02x:%02x" % (i, i)
        host = net.addHost("h%d" % i, ip=ip, mac=mac)
        hosts.append(host)

    # host 11
    ip = "10.0.%d.%d" % (1, 11)
    mac = "00:00:00:00:%02x:%02x" % (1, 11)
    host = net.addHost("h%d" % 11, ip=ip, mac=mac)
    hosts.append(host)

    info("*** Adding P4Switches (core)\n")
    for i in range(1, n_switches + 1):
        # read the network configuration
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = path + "/pot-polka/basic.json"
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
    for i in range(1, n_switches + 1):
        # read the network configuration
        path = os.path.dirname(os.path.abspath(__file__))
        json_file = path + "/pot-polka/basic.json"
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
    for i in range(0, n_switches):
        net.addLink(hosts[i], edges[i], bw=BW)
        net.addLink(edges[i], switches[i], bw=BW)

    lastSwitch = None

    for i in range(0, n_switches):
        switch = switches[i]

        if lastSwitch:
            net.addLink(lastSwitch, switch, bw=BW)
        lastSwitch = switch

    # host 11
    net.addLink(hosts[10], edges[0], bw=BW)

    info("*** Starting network\n")
    net.start()
    net.staticArp()

    # disabling offload for rx and tx on each host interface
    for host in hosts:
        host.cmd(f"ethtool --offload {host.name}-eth0 rx off tx off")
        host.cmd(f"ifconfig {host.name}-eth0 mtu 1500")

    info("*** Running CLI\n")
    # run_latency_test(net, 10, "./experiments", "method")
    # sleep(60)
    # run_iperf_test(net, 10, "./experiments", "method")
    # sleep(60)
    # run_fct_test(net, 10, "./experiments", "method")
    # sleep(60)
    # run_jitter_test(net, 10, "./experiments", "method")
    # sleep(60)
    # run_latency_test_background_traffic(net, 10, "./experiments", "method")
    # sleep(60)
    # run_latency_test_bigpacket(net, 10, "./experiments", "method")
    # sleep(60)
    CLI(net)

    #os.system("pkill -9 -f 'xterm'")
    #os.system("killall -9 bwm-ng")
    #os.system("killall -9 iperf")
    #os.system("killall -9 iperf3")
    #os.system("killall -9 ping")

    info("*** Stopping network\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    remote_controller = False
    topology(remote_controller)
