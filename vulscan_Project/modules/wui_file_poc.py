# -*- coding:utf-8 -*-
# 泛微OA9.0 任意文件上传

from .. import requestUtil

vul_path_9 = "/page/exportImport/uploadOperation.jsp"

def wui_file_poc(url):
    resp = requestUtil.get(url+vul_path_9)
    if resp.status_code == 200:
        return ["泛微OA9.0 任意文件上传", "uploadOperation.jsp"]
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
        return wui_file_poc(service.url)
    except:
        return []