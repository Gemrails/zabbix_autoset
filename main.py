#!/usr/bin/python
#coding=utf-8

import socket
import sys
import zabbix_set
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915, # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        group_name = "zabbix_agent"
    else:
        group_name = str(sys.argv[1])

    hostname = socket.gethostname()
    ip =  get_ip_address('eth0')
    rc = zabbix_set.main(group_name, hostname, ip)



