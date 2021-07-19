# -*- coding:utf-8 -*-
# 帆软报表8.0 任意文件读取

from VulnScanModel.models import VulnScan
from . import fineport_v8_file_poc


def exp(vuln: VulnScan, cmd, content=""):
    return fineport_v8_file_poc.fineport_file_poc(vuln.url, cmd, "exp")