# M-PolKA
M-PolKA (Multipath Polynomial Key-based Architecture)is a topology-agnostic multipath source routing architecture, which explores special properties from the RNS polynomial arithmetic and redefines the RNS coding for the representation of multipath routes. Thus, a myriad of new avenues will be open, from duplication of traffic through disjoint routes to multicast trees, could be properly represented. Therefore, M-PolKA is expected to deliver not only topology-agnostic solutions for controlability, but also answers to end-to-end (E2E) performance issues.

# RARE/FreeRtr

Freertr is a control plane: Router OS process speaks various network protocols, (re)encap packets, and exports forwarding tables to hardware switches. Basically, it is only necessary to install the Java Runtime Environment (JRE). Below is demonstrated how to install it on operating systems: Linux, Windows and macOS.

<p align="center">
  <img src="https://github.com/eversonscherrer/freertr/blob/main/M-PolKA/img/freertr.png">
</p>


# Requirement

Basic Linux/Unix knowledge
Service provider networking knowledge

# Operating system supported
This point exposes how to install freerouter and execute a edge-core topology with PolKA.

- Debian 10 (stable aka buster)
- Ubuntu 18.04 (Bionic beaver)
- Ubuntu 20.04 (Focal fossa)

## Install JRE
### Linux
For demonstration purposes, the Debian-based Linux installation was chosen.
```console
sudo apt-get install default-jre-headless --no-install-recommends
```

### MacOS
```console
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk list java
sdk install java 17.0.2-open
sdk default java 17.0.2-open
java -version
```

### Windows
In order to install the Windows version of Java, you need to visit the official Java website and download the Windows executable. After the download, check if your user has permission to install and perform the installation through the graphical environment. 

## Install Freertr
The freeRouter homepage is at freertr.net. Starting from this page, you'll find various resources such as source code (there is also a GitHub mirror), binaries, and other images that might be of your interest. From there we just download the freeRouter jar files.


```console
sudo wget freertr.net/rtr.jar
````

# Launch the Topology
Now it's time to run the topology, to run it, download all the hardware and software files that are in the repository, in the same folder.

**NOTE**
> To orchestrate the execution of the topology we use ```tmux```, if you don't have it installed, remember to install it.
```console
sudo apte-get install tmux
or
brew install tmux
````
There is a file called ```start-topology.sh``` in the repository. This file orchestrates the execution of all routers in a single run.

Notice
That file has two environment variables It needs to be defined ```RTR``` and ```HWSW``` these point to the path freertr and router files.  

```console
sudo chmod +x start-topology.sh
./start-topology.sh
```

# M-PolKA Topology
We used this diagram to describe a M-PolKA demo scenario.

![Topology](https://github.com/eversonscherrer/freertr/blob/main/M-PolKA/img/mpolka-topology.png)

# M-PolKA Experimentation

## 1 - To access the router, just access via telnet or ssh, in our demo, we use telnet.

```telnet <localhost> <port>```

For example, Access Router R5, to access another router, just change the port.
```console
telnet 127.0.0.1 2525
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
welcome
line ready
R5#
```

2. Check running-config for tunnel ipv4 M-PolKA in R5.

``` console
show running-config interface tunnel
```
```
R5#show running-config interface tunnel1
interface tunnel1
 description MPOLKA tunnel ipv4 from R5 -> R6
 tunnel vrf v1
 tunnel source loopback0
 tunnel destination 20.20.20.6
 tunnel domain-name 20.20.20.1 20.20.20.2 20.20.20.4 , 20.20.20.2 20.20.20.6 , 20.20.20.3 20.20.20.2 , 20.20.20.4 20.20.20.3 , 20.20.20.6 20.20.20.6 ,
 tunnel mode mpolka
 vrf forwarding v1
 ipv4 address 30.30.30.1 255.255.255.252
 no shutdown
 no log-link-change
 exit
```

3. Check running-config for tunnel ipv6 M-PolKA in R5.

``` console
show running-config interface tunnel2
```
```
R5#show running-config interface tunnel2
interface tunnel2
 description MPOLKA tunnel ipv6 from R5 -> R6
 tunnel vrf v1
 tunnel source loopback0
 tunnel destination 2020::6
 tunnel domain-name 2020::1 2020::2 2020::4 , 2020::2 2020::6 , 2020::3 2020::2 , 2020::4 2020::3 , 2020::6 2020::6 ,
 tunnel mode mpolka
 vrf forwarding v1
 ipv6 address 3030::1 ffff:ffff:ffff:ffff::
 no shutdown
 no log-link-change
 exit
```

4. Checking if the tunnels M-PolKA in R5 are up.

``` console
show interfaces summary | include tunnel1
```

```
R5#show interfaces summary | include tunnel
tunnel1    up     0    0      0
tunnel2    up     0    0      0
```

5. Chech M-PolKA polynomial RouteID.
```console
show mpolka routeid tunnel1
```
```
R5#show mpolka routeid tunnel1
iface      hop      routeid
ethernet1  5.5.5.2  00 00 00 00 00 00 04 15 2a 7c a6 d8 ba 68 32 df

index  coeff     poly   crc    equal
0      00010000  13023  13023  true
1      00010001  6      6      true
2      00010003  8      8      true
3      00010005  2      2      true
4      00010009  4      4      true
5      0001000f  56010  56010  true
6      00010011  1      1      true
7      0001001b  11283  11283  true
8      0001001d  61157  61157  true
9      0001002b  22410  22410  true
```

6. Connectivity test tunnel M-PolKA between R5 to R6

``` console
ping 30.30.30.2 /si 1111 /re 1111 /tim 11 /vrf v1 /int lo0 /mul
```

```
R5#ping 30.30.30.2 /si 1111 /re 1111 /tim 11 /vrf v1 /int lo0 /mul
pinging 30.30.30.2, src=20.20.20.5, vrf=v1, cnt=1111, len=1111, tim=11, gap=0, ttl=255, tos=0, sgt=0, flow=0, fill=0, 
sweep=false, multi=true, detail=false
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!...!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!
result=198%, recv/sent/lost/err=2206/1111/6/0, rtt min/avg/max/sum=0/2/128/14845, ttl min/avg/max=255/255/255, 
tos min/avg/max=0/0/0
```

# Conclusion
In this article you:
- you learned how to set up a M-PolKA environment deployment 

# References

https://ieeexplore.ieee.org/document/9738811

https://ieeexplore.ieee.org/document/9165501

https://chalk-thought-7ce.notion.site/PolKA-Project-7452bbe9bd294a9b88791ba9650a7069

https://wiki.geant.org/

http://www.freertr.net/