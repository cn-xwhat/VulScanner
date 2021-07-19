# -*- coding:utf-8 -*-
# docker未授权

from .. import requestUtil

def docker_poc(url):
    resp = requestUtil.get(url)
    if resp.status_code == 200:
        return ["docker未授权", "docker remote api未授权"]
    else:
        return []

def fingerprint(service):
    if service.port == 2375:
        return True

def poc(service):
    return docker_poc("http://%s:%s/info"%(service.ip, service.port))