# -*- coding:utf-8 -*-
# weblogic_wls9-async反序列化

from VulnScanModel.models import VulnScan
from . import weblogic_wls9_poc


def exp(vuln: VulnScan, cmd, content=""):
    print(vuln.specify)
    return weblogic_wls9_poc.wls9_cmd(vuln.url, cmd, "exp", vuln.specify)