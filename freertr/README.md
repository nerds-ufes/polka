# Requirement
Basic Linux/Unix knowledge
Service provider networking knowledge


# Overview
FreeRouter is a free, open source router control plane software, freeRouter besides Ethernet, is able to handle HDLC, X25, frame-relay, ATM encapsulation. Since it handles packets itself at the socket layer, it is independent of underlying Operation System capabilities. The command line tries to mimic the industry standards with one exception:

PolKA: Polynomial Key-based Architecture for Source Routing in Network Fabrics.

In order to be able to start a topology with PolKa. 

# Article objective
This article exposes how to install freerouter and execute a core topology with PolKA.

- Operating system supported:
  - Debian 10 (stable aka buster)
  - Ubuntu 18.04 (Bionic beaver)
  - Ubuntu 20.04 (Focal fossa)

# Diagram 
![rare-topology](https://user-images.githubusercontent.com/56919528/145196623-cc872b6d-7c48-4d83-9410-e6f2e1e23836.jpeg)

# Cookbook
1. Install you favorite operation system or use our virtualbox image:
  - Install your OS, like Ubuntu 18.04 MinimalCD 64-bit PC (amd64, x86_64) 64MB:
  ```
  http://archive.ubuntu.com/ubuntu/dists/bionic/main/installer-amd64/current/images/netboot/mini.iso
  ```
 
 ```console
  apt-get install default-jre-headless --no-install-recommends
  wget http://freerouter.nop.hu/rtr.jar
  tar xvf rtr.tar -C ~/freertr/
  ```
  
Or download our image:
  - In our example we will use the Ubuntu 20.04 installed as a VirtualBox VM:

  ![print VB](https://user-images.githubusercontent.com/56919528/145298486-9fe68011-3c7b-4eec-9680-91a8391b350d.png)

  ```
  https://drive.google.com/file/d/1tOLUS3VdMrvoLfts85mWcuk2IRK49yQ5/view?usp=sharing
  ```
2. Start & connect your VM as root.  
``` console
User: freertr
password: rtr
sudo -i
```

3. Install tmux and git:
``` console
apt install tmux -y
apt install git -y
```

4. Clone repository:
``` console
cd ~
git clone git@github.com:eversonscherrer/freertr.git
```

5. Set permission exec start/stop topology
``` console
cd freertr/polKa
chmod +x start.sh
chmod +x stop.sh
```
To run the topology `./start.sh` To stop the topology `./stop.sh`.
``` console
./start.sh
```

# Verification
1. Check telnet access for AMS0001@2121, FRA0001@2222, BUD0001@2323 and POZ0001@2424:

AMS0001 telnet access from Virtualbox VM guest via port 2121
``` console
# telnet 127.0.0.1 2121
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
welcome
line ready
AMS0001#
```

FRA0001 telnet access from Virtualbox VM guest via port 2222
``` console
# telnet 127.0.0.1 2222
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
welcome
line ready
FRA0001#
```

BUD0001 telnet access from Virtualbox VM guest via port 2323
``` console
# telnet 127.0.0.1 2323
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
welcome
line ready
BUD0001#
```

POZ0001 telnet access from Virtualbox VM guest via port 2424
``` console
# telnet 127.0.0.1 2424
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
welcome
line ready
POZ0001#
```

2. Check running-config for tunnel polka in RIO0001 to GVA0001
``` console
RIO0001#show running-config interface tunnel1
```
```
interface tunnel1
 description POLKA tunnel from RIO0001 -> GVA0001
 tunnel vrf v1
 tunnel source loopback0
 tunnel destination 20.20.20.7
 tunnel domain-name 20.20.20.1 20.20.20.2
 tunnel mode polka
 vrf forwarding v1
 ipv4 address 30.30.30.1 255.255.255.252
 no shutdown
 no log-link-change
 exit
!
```

``` console
RIO0001#show interfaces summary | include tunnel1
```

```
tunnel1    up     0      0      0
```

3. Check running-config for tunnel polka in GVA0001 to RIO0001
``` console
GVA0001#show running-config interface tunnel1
```
```
interface tunnel1
 description POLKA tunnel from GVA0001 -> RIO0001
 tunnel vrf v1
 tunnel source loopback0
 tunnel destination 20.20.20.11
 tunnel domain-name 20.20.20.2 20.20.20.1
 tunnel mode polka
 vrf forwarding v1
 ipv4 address 30.30.30.2 255.255.255.252
 no shutdown
 no log-link-change
 exit
!
```

``` console
GVA0001#show interfaces summary | include tunnel1
```

```
tunnel1    up     0      0      0
```

4. Show RIO0001 polka polynomial table
```console
RIO0001#show polka routeid tunnel1
```
```
mode  routeid
hex   00 00 00 00 00 00 41 3b fd 39 6d 38 a0 07 71 39
poly  1000001001110111111110100111001011011010011100010100000000001110111000100111001

index  coeff     poly   crc    equal
0      00010000  28985  28985  true
1      00010001  4      4      true
2      00010003  7      7      true
3      00010005  2      2      true
4      00010009  3      3      true
5      0001000f  61482  61482  true
6      00010011  60173  60173  true
7      0001001b  0      0      true
8      0001001d  59032  59032  true
9      0001002b  2564   2564   true
10     0001002d  23723  23723  true
11     00010039  44005  44005  true
12     0001003f  60401  60401  true
13     00010047  23239  23239  true
14     0001004b  45928  45928  true
15     00010053  48139  48139  true
16     00010059  60634  60634  true
17     00010063  51307  51307  true
18     00010065  15510  15510  true
19     0001006f  52396  52396  true
```
5. Show GVA0001 polka polynomial table
```console
RIO0001#show polka routeid tunnel1
```
```
mode  routeid
hex   00 00 00 00 00 00 70 06 06 50 8c 16 8b ae 71 e5
poly  1110000000001100000011001010000100011000001011010001011101011100111000111100101

index  coeff     poly   crc    equal
0      00010000  29157  29157  true
1      00010001  11     11     true
2      00010003  3      3      true
3      00010005  4      4      true
4      00010009  1      1      true
5      0001000f  9414   9414   true
6      00010011  59245  59245  true
7      0001001b  59453  59453  true
8      0001001d  25591  25591  true
9      0001002b  41976  41976  true
10     0001002d  8957   8957   true
11     00010039  0      0      true
12     0001003f  11798  11798  true
13     00010047  31110  31110  true
14     0001004b  64183  64183  true
15     00010053  16381  16381  true
16     00010059  13158  13158  true
17     00010063  28832  28832  true
18     00010065  21926  21926  true
19     0001006f  17893  17893  true
```

6. Connectivity test tunnel polka between RIO0001 to GVA0001
``` console
RIO0001#ping 30.30.30.2 /vrf v1
```
``` 
pinging 30.30.30.2, src=null, vrf=v1, cnt=5, len=64, tim=1000, gap=0, ttl=255, tos=0, flow=0, fill=0, sweep=false, multi=false, detail=false
!!!!!
result=100%, recv/sent/lost/err=5/5/0/0, rtt min/avg/max/total=1/1/2/7
```

7. Connectivity test tunnel polka between  GVA0001 to RIO0001
``` console
GVA0001#ping 30.30.30.1 /vrf v1
```
```
pinging 30.30.30.1, src=null, vrf=v1, cnt=5, len=64, tim=1000, gap=0, ttl=255, tos=0, flow=0, fill=0, sweep=false, multi=false, detail=false
!!!!!
result=100%, recv/sent/lost/err=5/5/0/0, rtt min/avg/max/total=1/1/2/7
```
8. Now we are going to debug the longest path and the shortest path as shown in the screenshot.
 
![rare-topology-Tunnel](https://user-images.githubusercontent.com/56919528/145882530-2bb1b5a6-38e5-442f-b6d0-8b90e4e0b4cb.png)


9. Shortest Path 
In the initial setup, we had already enabled the shortest path. Below you can see the debug of this configuration.

Router RIO0001
```
RIO0001#show running-config | section tunnel1
```

![Screen Shot 2021-12-13 at 19 09 13](https://user-images.githubusercontent.com/56919528/145897059-d2f029ba-1bed-427f-8461-7e75bf89dc9a.png)

Router GVA0001
```
GVA0001#show running-config | section tunnel1
```

![Screen Shot 2021-12-13 at 19 09 46](https://user-images.githubusercontent.com/56919528/145897117-0fb7820d-6b42-42c7-8106-a19975159b30.png)

In this screenshot we can see the debug in the shortest path of the packages

going  - RIO0001 -> AMS0001 -> FRA0001 -> GVA0001 - echo request

back - GVA0001 -> FRA0001 -> AMS0001 -> RIO0001 - echo replay

I used the following commands to debug the path.
```console
RIO0001#ping 30.30.30.2 /vrf v1 /size 1111 /repeat 111111
```
and 
```console
RIO0001#display interfaces traffic
AMS0001#display interfaces traffic
FRA0001#display interfaces traffic
BUD0001#display interfaces traffic
POZ0001#display interfaces traffic
GVA0001#display interfaces traffic
```

Note in this screenshot that only the shortest path routers have traffic.

![Screen Shot 2021-12-13 at 19 25 59](https://user-images.githubusercontent.com/56919528/145899115-084f97fd-f954-4de4-90d1-a664c3f8544f.png)


11. Longest Path
To use the longest path we will have to reconfigure the domain name of the tunnel.

Router RIO0001

```console
RIO0001#configure terminal
RIO0001(cfg)#interface tunnel1
RIO0001(cfg-if)#tunnel domain-name 20.20.20.1 20.20.20.4 20.20.20.3 20.20.20.2
RIO0001(cfg-if)#end
RIO0001#write
RIO0001#reload warm
```

Router GVA0001

```console
GVA0001#configure terminal
GVA0001(cfg)#interface tunnel1
GVA0001(cfg-if)#tunnel domain-name 20.20.20.2 20.20.20.3 20.20.20.4 20.20.20.1
GVA0001(cfg-if)#end
GVA0001#write
GVA0001#reload warm
```

Router RIO0001
```
RIO0001#show running-config | section tunnel1
```
note below the modification of the path at the source on router RIO.

![Screen Shot 2021-12-13 at 19 43 10](https://user-images.githubusercontent.com/56919528/145900748-5edfac6d-7f1a-4f6a-bd26-9aa020e0932b.png)

Router GVA0001
```
GVA0001#show running-config | section tunnel1
```

note below the modification of the path at the source on router GVA0001.

![Screen Shot 2021-12-13 at 19 55 34](https://user-images.githubusercontent.com/56919528/145902171-2a91886c-f632-447b-ad5c-d6fbb65f2e54.png)


I used the following commands to debug the path.

```console
RIO0001#ping 30.30.30.2 /vrf v1 /size 1111 /repeat 111111
```
and 
```console
RIO0001#display interfaces traffic
AMS0001#display interfaces traffic
FRA0001#display interfaces traffic
BUD0001#display interfaces traffic
POZ0001#display interfaces traffic
GVA0001#display interfaces traffic
```

going - RIO0001 -> AMS0001 -> POZ0001 -> BUD0001 -> FRA0001 -> GVA0001 - echo request
back - GVA0001 -> FRA0001 -> BUD0001 -> POZ0001 -> AMS0001 -> RIO0001 - echo replay

In this screenshot we can see the debug in the longest path of the packages

![Screen Shot 2021-12-13 at 19 59 14](https://user-images.githubusercontent.com/56919528/145902514-22b74983-b326-4114-998b-259f7572e1c2.png)


# Conclusion
In this article you:
- had a showcase on how to implement a fully disaggregated RARE/freeRtr
- you learned how to set up a PolKA environment deployment 

# References

https://ieeexplore.ieee.org/document/9165501

https://chalk-thought-7ce.notion.site/PolKA-Project-7452bbe9bd294a9b88791ba9650a7069

https://wiki.geant.org/

http://www.freertr.net/
