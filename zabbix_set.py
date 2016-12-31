#!/usr/bin/python
#coding=utf-8

import json

from zabbix_lib import zs_constant
from zabbix_lib.api import ZabbixAPI
from zabbix_lib.api import ZabbixAPIException


class zabbix_go(object):
    def __init__(self, z_server):
        self.zapi = ZabbixAPI(z_server, user='xxx', password='xxxxx')

    def api_v(self):
        return self.zapi.api_version()

    def load_xml(self, xml):
        rule = json.loads(file(xml))
        return rule

    def create_group(self, group_name):                                                         #创建组
        if not self.zapi.hostgroup.exists(name=group_name):
            self.zapi.hostgroup.create(name=group_name)
        return group_name

    def get_hostgroups(self, group_name):
        return self.zapi.hostgroup.get(search={"name":group_name }, output="extend")

    def get_templates_by_names(self, template_names):
        return self.zapi.template.get(filter={"host": template_names})

    def get_temp_list(self):
        temp_list = []
        for temp in zs_constant.ord_name:
            self.get_templates_by_names(temp)
            temp_list.append(self.get_templates_by_names(temp)[0].get("templateid"))
        return temp_list

    def create_host(self, group_name, host_name, ip):
        groups = self.get_hostgroups(group_name)
        group_id = groups[0].get("groupid")
        temp_list = self.get_temp_list()

        host_name = host_name.lower()
        ip_tail = ip.split(".")[-1]
        domain = host_name + '-' + ip_tail

        try:
            rc = self.zapi.host.create(host=domain, interfaces=[{
                "type"  :   1,
                "main"  :   1,
                "useip" :   1,
                "ip"    :   ip,
                "dns"   :   "",
                "port"  :   '10050'
            }], groups=[{"groupid":group_id}], templates = temp_list)
        except ZabbixAPIException , e:
            print "already exits"

#res = zapi . host . update ( hostid = hostid , templates = template_new )

def main(group_name, hostname, ip):
    try:
        z_go = zabbix_go(zs_constant.ZABBIX_SERVER)
        z_go.create_host(z_go.create_group(group_name), hostname, ip)
    except Exception, e:
        print e
        return None

if __name__ == '__main__':
    z_go = zabbix_go(zs_constant.ZABBIX_SERVER)
    print z_go.create_group('test_group')
    print z_go.get_hostgroups('devops')
    print z_go.api_v()
    z_go.create_host(z_go.create_group('test_group'), 'test-host', '10.18.99.99')

