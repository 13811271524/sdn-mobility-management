#!/usr/bin/python

import re
import os
from mininet.cli import CLI
from mininet.log import setLogLevel, info,error
from mininet.net import Mininet
from mininet.link import Intf,Link
from mininet.topolib import TreeTopo
from mininet.util import quietRun
from mininet.node import Host,RemoteController, OVSKernelSwitch

if __name__ == "__main__":
    setLogLevel("info")
    OVSKernelSwitch.setup()
    intfName_1 = "wlan0" 
    info("****checking****", intfName_1, '\n')
    info("****creating network****\n")

    net = Mininet()

    switch_1 = net.addSwitch('s1')
    switch_2 = net.addSwitch('s2')
    switch_3 = net.addSwitch('s3')
    switch_4 = net.addSwitch('s4')
    switch_5 = net.addSwitch('s5')
    switch_6 = net.addSwitch('s6')
    switch_7 = net.addSwitch('s7')
    
    h0 = net.addHost('h0')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    c0 = net.addController('c0',controller=RemoteController, ip = "10.108.100.195")

    net.addLink(switch_1, switch_2, 1, 1)
    net.addLink(switch_1, switch_3, 2, 1)
    net.addLink(switch_1, switch_4, 3, 1)

    net.addLink(switch_2, switch_5, 2, 1)
    net.addLink(switch_2, switch_6, 3, 1)

    net.addLink(switch_3, switch_5, 2, 3)
    net.addLink(switch_3, switch_6, 3, 2)

    net.addLink(switch_4, switch_7, 2, 1)

    net.addLink(switch_5, h0,4,0)
    net.addLink(switch_6, h1,3,0)
    net.addLink(switch_7, h2,2,0)
    net.addLink(switch_6, h0,4,1)

    info("*****Adding hardware interface ",intfName_1, "to switch:" ,switch_1.name, '\n')
    _intf_1 = Intf(intfName_1, node = switch_5, port =  2)
    info("Node: you may need to reconfigure the interfaces for the Mininet hosts:\n",   net.hosts, '\n')

    net.start()  
    h1.setIP("172.16.0.2/24")
    h0.setIP("192.168.0.3",24,'h0-eth0')
    h0.setIP("192.168.0.3",24,'h0-eth1')
    h2.setIP("10.0.0.2/24")
    h0.setMAC("8e:78:b3:7c:d4:81",'h0-eth0')
    h0.setMAC("8e:78:b3:7c:d4:81",'h0-eth1')
    h1.setMAC("32:5a:3f:9c:13:75")
    h2.setMAC("66:26:30:21:ed:8f")
    h0.setDefaultRoute('dev h0-eth0 via 192.168.0.1')
    h0.setDefaultRoute('dev h0-eth1 via 192.168.0.1')
    h1.setDefaultRoute('dev h1-eth0 via 172.16.0.1')
    h2.setDefaultRoute('dev h2-eth0 via 10.0.0.1')
    os.system('bash /home/mininet/test.sh')
    CLI(net)    
    net.stop() 
