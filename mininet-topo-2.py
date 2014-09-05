#!/usr/bin/python

import re
import os
import time 
from mininet.cli import CLI
from mininet.log import setLogLevel, info,error,output
from mininet.net import Mininet
from mininet.link import Intf,Link
from mininet.topolib import TreeTopo
from mininet.util import quietRun,dumpNodeConnections
from mininet.node import Host,RemoteController, OVSKernelSwitch,OVSSwitch
from mininet.term import makeTerms

def configLinkStatus( src, dst, status ):
    connections = src.connectionsTo( dst )
    if len( connections ) == 0:
        error( 'src and dst not connected: %s %s\n' % ( src, dst) )
    for srcIntf, dstIntf in connections:
        print srcIntf,dstIntf
        result = srcIntf.ifconfig( status )
        if result:
            error( 'link src status change failed: %s\n' % result )
        result = dstIntf.ifconfig( status )
        if result:
            error( 'link dst status change failed: %s\n' % result )

h0 = Host( 'h0' )
h1 = Host( 'h1' )
h2 = Host( 'h2' )
h3 = Host( 'h3' )

s0 = OVSKernelSwitch( 's0' ,inNamespace=False )
s1 = OVSKernelSwitch( 's1' ,inNamespace=False )
s2 = OVSKernelSwitch( 's2', inNamespace=False  )
s3 = OVSKernelSwitch( 's3' ,inNamespace=False ) 

c0 = RemoteController( 'c0', ip = '10.108.100.195' ) 
c1 = RemoteController( 'c1', ip = '10.108.100.248' ) 
c2 = RemoteController( 'c2', ip = '10.108.102.176' ) 
c3 = RemoteController( 'c3', ip = '10.108.101.48' )

l1 = Link( h0, s1 )
Link( h1, s1 ) 
Link( h2, s2 )
Link( h3, s3 )
Link( s0, s1 )
Link( s0, s2 )
Link( s0, s3 )

h0.setIP( '10.1.0.1/16' )
h1.setIP( '10.1.0.2/16' )
h2.setIP( '10.2.0.1/16' )
h3.setIP( '10.3.0.1/16' )

print h0.cmd('ifconfig')
c0.start()
c1.start()
c2.start()
c3.start()

s0.start( [ c0 ] )
s1.start( [ c1 ] )
s2.start( [ c2 ] )
s3.start( [ c3 ] )

dumpNodeConnections([s0,s1,s2,s3,h0,h1,h2,h3])
temp = l1.intf1
l1.delete()

h0.intfs = {}
h0.ports = {}
h0.nameToIntf = {} 

l1.intf1 = None
#for intf in s1.intfList():
#	if intf.link and intf.link.intf1.name == 'h0-eth0':
#		intf.link.intf1 = None

l2 = Link(s2,h0,s2.newPort(),0)

h0.setIP( '10.1.0.1/16' )
h0.setMAC(temp.mac)
h0.intfList()[0].mac = temp.mac
h0.intfList()[0].ip = temp.ip

print s2.cmd('ovs-vsctl add-port s2 s2-eth3')
print '**********'
print h0.cmd('ifconfig')

dumpNodeConnections([s0,s1,s2,s3,h0,h1,h2,h3])
#output('%s\n' % repr(h0))
#makeTerms([s2],'xterm')

string = raw_input()
while string != 'exit':
    string = raw_input()

s0.stop()
s1.stop()
s2.stop()
s3.stop()

c0.stop() 
c1.stop()
c2.stop()
c3.stop()
