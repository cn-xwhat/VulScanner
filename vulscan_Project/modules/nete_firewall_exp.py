# -*- coding:utf-8 -*-
# 奇安信 网康下一代防火墙RCE

from VulnScanModel.models import VulnScan
from . import nete_firewall_poc


def exp(vuln: VulnScan, cmd, content=""):
    return nete_firewall_poc.firewall_rce(vuln.url, cmd)