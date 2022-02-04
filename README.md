# PolKA - Polynomial Key-based Source Routing

Source routing (SR) is a prominent alternative to table-based routing for reducing the number of network states. However, traditional SR approaches, based on Port Switching, still maintain a state in the packet by using a header rewrite operation. The residue number system (RNS) is a promising way of executing fully stateless SR, in which forwarding decisions at core nodes rely on a simple modulo operation over a route label. Nevertheless, such operation over integer arithmetic is not natively supported by commodity network hardware. Thus, we propose a novel RNS-based SR scheme, named PolKA, that explores binary polynomial arithmetic using Galois field (GF) of order 2. We evaluate PolKA in comparison to Port Switching by implementing emulated and hardware prototypes using P4 architecture. Results show that PolKA can achieve equivalent performance, while providing advanced routing features, such as fast failure reaction and agile path migration.

![Example of polka_sr](./mininet/figures/architecture.png)

PolKA is a RNS-based SR scheme that explores the Chinese remainder theorem (CRT) for polynomials. As shown in figure, the architecture is composed of: (i) edge nodes, (ii) core nodes, and (iii) an SDN Controller, responsible for configuring the nodes. The SR relies on three polynomials over GF(2): (i) nodeID: a fixed identifier assigned to core nodes by the Controller in a network configuration phase; (ii) portID: an identifier assigned to the output ports of each core node; and (iii) routeID: a route identifier, calculated by the Controller and embedded into the packets by the edge nodes.

Figure shows an example of PolKA SR for a path composed of three nodes, which received their nodeIDs from the Controller: s1(t) = t + 1 (or 11), s2(t) = t2 + t + 1 (or 111), s3(t) = t3 + t + 1 (or 1011). For this path, the portIDs are: o1(t) = 1, o2(t) = t (or 10), o3(t) = t2 + t (or 110). The routeID calculated by the Controller is R(t) = t4 (or 10000). Thus, each node can calculate the portID using a modulo operation. For example: at s3, o3(t) = < 10000 >1011 = 110.

## Preparing the environment

To download the VM image, we have to use the following link:

[[6.7GB Size] - Lubuntu 20.04 x64](https://drive.google.com/file/d/1oozRqFO2KjjxW0Ob47d6Re4i6ay1wdwg/view?usp=sharing) - Mininet-WiFi with P4 (_pass: wifi_)

After downloading, we have to perform the login (user: wifi, pass: wifi) and clone the repository as follows:

```sh
wifi@wifi-virtualbox:~$ git clone https://github.com/nerds-ufes/polka.git
```

## Using PolKA

* [Mininet+P4](./mininet)
* [Freertr](./freertr)

# References

https://ieeexplore.ieee.org/document/9492363

https://ieeexplore.ieee.org/document/9165501
