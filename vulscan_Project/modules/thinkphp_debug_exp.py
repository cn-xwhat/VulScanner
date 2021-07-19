# -*- coding:utf-8 -*-
# Thinkphp debug命令执行

from .. import requestUtil
from . import thinkphp_debug_poc

def exp(service, cmd, content=""):
    print(cmd)
    return thinkphp_debug_poc.thinphp_debug(service.url, cmd)