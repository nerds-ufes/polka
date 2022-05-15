#!/usr/bin/python

from p4app import P4Mininet, P4Program
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg
from mininet.util import dumpNodeConnections, custom
from mininet.cli import CLI

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

from util.monitor import monitor_devs_ng, monitor_cpu

# import shlex
import sys

# import os.shutil


class LinearTopo(Topo):
    def __init__(self, n_host, **opts):
        Topo.__init__(self, **opts)

        # linkopts = dict(bw=1, cls=TCLink)
        linkopts = dict()
        n_switch = 1
        switches = []

        for i in range(1, n_switch + 1):
            switch = self.addSwitch("s%d" % i)
            switches.append(switch)

        for i in range(1, n_host + 1):
            ip = "10.0.%d.%d" % (i, i)
            mac = "00:00:00:00:%02x:%02x" % (i, i)
            host = self.addHost("h%d" % i, ip=ip, mac=mac)
            self.addLink(host, switches[0], **linkopts)

        # Connection between core switches
        # lastSwitch = None
        # for i in range(0, n_switch):
        #    switch = switches[i]
        #    if lastSwitch:
        #        self.addLink(lastSwitch, switch, **linkopts)
        #    lastSwitch = switch


class FabricTopo(Topo):
    def __init__(self, n, core_file, edge_file, **opts):
        Topo.__init__(self, **opts)

        switches = []
        core_prog = P4Program(core_file)
        edge_prog = P4Program(edge_file)

        for i in range(1, n + 1):
            ip = "10.0.%d.%d" % (i, i)
            mac = "00:00:00:00:%02x:%02x" % (i, i)
            host = self.addHost("h%d" % i, ip=ip, mac=mac)
            edge = self.addSwitch("e%d" % i, program=edge_prog)
            switch = self.addSwitch("s%d" % i, program=core_prog)
            self.addLink(host, edge)
            self.addLink(edge, switch)

            if i == 1:
                # Add host for 0 hop
                ip = "10.0.1.11"
                mac = "00:00:00:00:01:0b"
                host = self.addHost("h11", ip=ip, mac=mac)
                self.addLink(host, edge)

            switches.append(switch)

            # Connection between core switches
        lastSwitch = None
        for i in range(0, n):
            switch = switches[i]

            # if (i==0):
            # switch0 = self.addSwitch('s0', program=core_prog)
            # self.addLink( switches[0], switch0)

            if lastSwitch:
                self.addLink(lastSwitch, switch)
            lastSwitch = switch


def config_network(bw, n_host):

    n_switch = 1
    program = "polka-core.p4"

    topo = LinearTopo(n_host=n_host)
    link = custom(TCLink, bw=bw)
    # net = P4Mininet(
    #    program="polka.p4",
    #    topo=topo,
    #    host=CPULimitedHost,
    #    link=TCLink,
    #    enable_debugger=True,
    # )
    net = P4Mininet(program=program, topo=topo, link=link, enable_debugger=True)
    net.start()

    print("Switch: Configuration")

    for i in range(1, n_switch + 1):
        sw = net.get("s%d" % i)
        fname = "cfg/polka-fabric" + "/s%d" % i + "-commands.txt"
        print("Configuring switch: " + "s%d" % i)
        print("Config filename: " + fname)
        with open(fname, "r") as file:
            cmd = file.read()
        sw.command(cmd)

    return net


def main():
    lg.setLogLevel("info")

    if len(sys.argv) > 1:
        n_host = int(sys.argv[1])
    else:
        n_host = 3

    print("Setting-up a {}-hosts linear topology".format(n_host))

    # testdir = "test"  # output directory

    bw = 10

    net = config_network(bw, n_host=n_host)

    sleep(5)

    # os.system("killall -9 iperf")
    # os.system("killall -9 ping")

    start = time()

    CLI(net)
    net.stop()
    end = time()
    print("Experiment took {.3f} seconds".format(end - start))


if __name__ == "__main__":
    main()
