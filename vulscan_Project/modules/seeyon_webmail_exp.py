# -*- coding:utf-8 -*-
# 致远OA_webmail.do任意文件下载

from VulnScanModel.models import VulnScan
from . import seeyon_webmail_poc


def exp(vuln: VulnScan, cmd, content=""):
    return seeyon_webmail_poc.webmail_download(vuln.url, cmd, "exp")