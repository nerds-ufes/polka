# Overview

FreeRouter is a free, open source router control plane software. For nostalgic and networkers from prehistoric era (like me), freeRouter besides Ethernet, is able to handle HDLC, X25, frame-relay, ATM encapsulation. Since it handles packets itself at the socket layer, it is independent of underlying Operation System capabilities. We will see in the next articles how freeRouter subtlety leverage this inherently independence to connect different data-plane such as OpenFlow, P4 and other possible data-plane that would appear in the near future.

# Let's hands-on Freertr+PolKA

All of our Freertr with PolKA examples are mimicing the RARE Topology. 

* [Simple Routing (Static Route)](./rare-simple-test/)
* [Policy Based Routing (PBR)](./rare-pbr-test/)

# References

https://ieeexplore.ieee.org/document/9165501

https://chalk-thought-7ce.notion.site/PolKA-Project-7452bbe9bd294a9b88791ba9650a7069

https://wiki.geant.org/

http://www.freertr.net/
