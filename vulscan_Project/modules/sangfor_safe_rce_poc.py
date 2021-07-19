# -*- coding:utf-8 -*-
# 深信服行为感知系统RCE

from .. import requestUtil

def sangfor_rce(url):
    resp = requestUtil.get(url+"/tool/log/c.php")
    if not resp.status_code == 200:
        return ["深信服行为感知系统RCE", "path:/tool/log/c.php"]
    else:
        return []


def fingerprint(service):
    resp = requestUtil.get(service.url)
    if "isHighPerformance : !!SFIsHighPerformance" in resp.text:
        return True


def poc(service):
    return sangfor_rce(service.url)
