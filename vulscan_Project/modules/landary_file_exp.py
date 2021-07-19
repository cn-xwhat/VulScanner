# -*- coding:utf-8 -*-
# 蓝凌OA 任意文件读取

from VulnScanModel.models import VulnScan
from . import landary_file_poc


def exp(vuln: VulnScan, cmd, content=""):
    return landary_file_poc.read_file(vuln.url, cmd)