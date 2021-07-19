# -*- coding:utf-8 -*-
# axis2弱密码

from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan

def fingerprint(service):
    try:
        if service.url and "Apache-Coyote" in service.server:
            resp_1 = requestUtil.get(service.url+"/axis2/")
            resp_2 = requestUtil.get(service.url+"/axis2-admin/")
            if resp_1.status_code == 200:
                return "/axis2/axis2-admin/"
            elif resp_2.status_code == 200:
                return "/axis2-admin/"
    except:
        return False

def poc(service: ServiceScan):
    try:
        if True:
            resp = requestUtil.post(service.url+service.speciality+"login", data="userName=admin&password=axis2&submit=+Login+")
            print(resp.text)
            if "Tools" in resp.text:
                return (["axis2弱密码", "用户名: admin<br>密码: axis2"], service.speciality)
    except:
        return []