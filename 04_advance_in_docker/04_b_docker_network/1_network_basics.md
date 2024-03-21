
# network basic concept

## 1 network namespace

Network namespaces can virtualize network stacks, and each network namespace has its own resources, such as network interfaces, IP addresses, routing tables, tunnels, firewalls, etc. For example, rules added to a network namespace by iptables will only affect traffic entering and leaving that namespace.

## 2 how communication between two network namespace
use **veth pair**, Create a veth pair and attach each side to the appropriate namespace, then the two namespace can communicate with each other. Veth is a type of virtual ethernet interface that is always created as a pair. Veth can be thought of as a 'virtual crossover cable', it creates two virtual NICs that are connected

## 3 how to communication within network namepsace which is more than 2?
1. create a object which is called **virtual bridge**
2. in every namespace, use veth pair to attach each side to the bridge. then use the briage to link different namespace.

## 4 how to communication between  a cumtom created namespace and host namespace ?
1. just assign a ip address to the virtual bridge to launch its route function. then the virtual bridge can be regarged a network card. can communicate with host.
2. then the created namespace within the virtual bridge can communicate with host.


# docker network


## 1 docker contrainers within the default docker bridge(docker0), can communicate with each other by ip address.
When you install Docker Engine it creates a bridge network automatically. This network corresponds to the docker0 bridge(a virtual bridge) that Docker Engine has traditionally relied on. 
~~~
ifconfig

docker0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.1  netmask 255.255.0.0  broadcast 172.17.255.255
        inet6 fe80::42:60ff:fef6:c3ec  prefixlen 64  scopeid 0x20<link>
        ether 02:42:60:f6:c3:ec  txqueuelen 0  (Ethernet)
~~~

When you launch a new container with docker run it automatically connects to this bridge network. 


~~~
sudo docker run -itd --name u1 ubuntu:22.04 /bin/bash
sudo docker run -itd --name u2 ubuntu:22.04 /bin/bash
~~~

~~~
sudo docker inspect u1 | tail -n 20

           "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "47899f2b9d9f"
                    ],
                    "MacAddress": "02:42:ac:11:00:06",
                    "NetworkID": "4e8048fe7b101c9f4ed1c4772d39dda3d253ffd74d76cacfb2b3052cbc81f64f",
                    "EndpointID": "6a0b7a85f539d4b0f9f1574cc8e0820fb86f94481928de7ac98bd566ac42395d",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.6",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "DriverOpts": null,
                    "DNSNames": null


sudo docker inspect u2 | tail -n 30

           "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "c26e17ca26e0"
                    ],
                    "MacAddress": "02:42:ac:11:00:07",
                    "NetworkID": "4e8048fe7b101c9f4ed1c4772d39dda3d253ffd74d76cacfb2b3052cbc81f64f",
                    "EndpointID": "2073ed7f14262816943740dbdba99545f083ff0be513a7bc2022a4cefef4d755",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.7",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "DriverOpts": null,
                    "DNSNames": null
                }
~~~

**conclusion1: in u1, you can communicate with u2 by ip address, but not the service name.**

~~~
sudo docker exec -it u1 bash

root@47899f2b9d9f:/# apt-get update
root@47899f2b9d9f:/# apt install iputils-ping
~~~

~~~
root@47899f2b9d9f:/# ping 172.17.0.7
PING 172.17.0.7 (172.17.0.7) 56(84) bytes of data.
64 bytes from 172.17.0.7: icmp_seq=1 ttl=64 time=0.155 ms
64 bytes from 172.17.0.7: icmp_seq=2 ttl=64 time=0.105 ms
64 bytes from 172.17.0.7: icmp_seq=3 ttl=64 time=0.104 ms
64 bytes from 172.17.0.7: icmp_seq=4 ttl=64 time=0.062 ms
64 bytes from 172.17.0.7: icmp_seq=5 ttl=64 time=0.092 ms
64 bytes from 172.17.0.7: icmp_seq=6 ttl=64 time=0.106 ms
64 bytes from 172.17.0.7: icmp_seq=7 ttl=64 time=0.079 ms

root@47899f2b9d9f:/# ping u2
ping: u2: No address associated with hostname
~~~

communication by ip address in docker is risk. why?
~~~
sudo docker rm -f u2
sudo docker run -itd --name u3 ubuntu:22.04 /bin/bash
~~~

if u2 stopped with a bad reason, a new created contrainer will have the same ip-address 

~~~
sudo docker inspect u3 | tail -n 30

            "Networks": {
                "bridge": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "ed016324424b"
                    ],
                    "MacAddress": "02:42:ac:11:00:07",
                    "NetworkID": "4e8048fe7b101c9f4ed1c4772d39dda3d253ffd74d76cacfb2b3052cbc81f64f",
                    "EndpointID": "bba77ac079fcc1454fd576cd9a85139ab39a5f064ff9e10a697b7c0e317585f3",
                    "Gateway": "172.17.0.1",
                    "IPAddress": "172.17.0.7",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "DriverOpts": null,
                    "DNSNames": null
                }
            }

~~~

You cannot remove this default bridge network, but you can create new ones using the network create command.

# create a custom network bridge, put the related container in that network, then you can communicate with each using container IP addresses or container names.

You can create custom, user-defined networks, and connect multiple containers to the same network. Once connected to a user-defined network, containers can communicate with each other using container IP addresses or container names.

The following example creates a network using the bridge network driver and running a container in the created network: 
~~~
sudo docker network create -d bridge my-net

(base) yujiang@yujiang-System-Product-Name:~$ sudo docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
4e8048fe7b10   bridge    bridge    local
5120efc2bb71   host      host      local
d297a3142e7c   my-net    bridge    local
b0269fb163ed   none      null      local
~~~

~~~
sudo docker run -itd --name u4 --network=my-net ubuntu:22.04 /bin/bash
sudo docker run -itd --name u5 --network=my-net ubuntu:22.04 /bin/bash
~~~


~~~
sudo docker inspect u4 | tail -n 30

"Networks": {
                "my-net": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "3f7bd73f6a83"
                    ],
                    "MacAddress": "02:42:ac:12:00:02",
                    "NetworkID": "d297a3142e7cd8ec6e41a0c392f9cba15b44b9bb3009f3867beff3c2b85c9f66",
                    "EndpointID": "65f350639142f66858b6db0eee832c580ccbba1a5bf2431172379ad3cfed2e88",
                    "Gateway": "172.18.0.1",
                    "IPAddress": "172.18.0.2",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "DriverOpts": null,
                    "DNSNames": [
                        "u4",
                        "3f7bd73f6a83"
                    ]
                }


sudo docker inspect u5 | tail -n 30

"Networks": {
                "my-net": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "aa69f0fb8d0f"
                    ],
                    "MacAddress": "02:42:ac:12:00:03",
                    "NetworkID": "d297a3142e7cd8ec6e41a0c392f9cba15b44b9bb3009f3867beff3c2b85c9f66",
                    "EndpointID": "4c76637821285406962f60d5a34bff1d40d955ed39cb28f0d17c22a30368a847",
                    "Gateway": "172.18.0.1",
                    "IPAddress": "172.18.0.3",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "DriverOpts": null,
                    "DNSNames": [
                        "u5",
                        "aa69f0fb8d0f"
                    ]
                }

~~~

check the communication path

~~~
sudo docker exec -it u1 bash

root@47899f2b9d9f:/# apt-get update
root@47899f2b9d9f:/# apt install iputils-ping
root@3f7bd73f6a83:/# ping 172.18.0.3


PING 172.18.0.3 (172.18.0.3) 56(84) bytes of data.
64 bytes from 172.18.0.3: icmp_seq=1 ttl=64 time=0.178 ms
64 bytes from 172.18.0.3: icmp_seq=2 ttl=64 time=0.089 ms
64 bytes from 172.18.0.3: icmp_seq=3 ttl=64 time=0.059 ms
64 bytes from 172.18.0.3: icmp_seq=4 ttl=64 time=0.090 ms
64 bytes from 172.18.0.3: icmp_seq=5 ttl=64 time=0.083 ms
64 bytes from 172.18.0.3: icmp_seq=6 ttl=64 time=0.090 ms


root@3f7bd73f6a83:/# ping u5
PING u5 (172.18.0.3) 56(84) bytes of data.
64 bytes from u5.my-net (172.18.0.3): icmp_seq=1 ttl=64 time=0.038 ms
64 bytes from u5.my-net (172.18.0.3): icmp_seq=2 ttl=64 time=0.108 ms
64 bytes from u5.my-net (172.18.0.3): icmp_seq=3 ttl=64 time=0.048 ms
64 bytes from u5.my-net (172.18.0.3): icmp_seq=4 ttl=64 time=0.083 ms
64 bytes from u5.my-net (172.18.0.3): icmp_seq=5 ttl=64 time=0.121 ms
64 bytes from u5.my-net (172.18.0.3): icmp_seq=6 ttl=64 time=0.106 ms
~~~

**in custom network bridge, containers can communicate with each other using container IP addresses or container names.**  


## 3 other option  of network for containers

* host: use the host (bridge) as the bridge, every container share the same ip address. the nation of port mapping is disable.
* none: no bridge
* container: use a container's network namespace as my network, sharing the same network namespace. 

