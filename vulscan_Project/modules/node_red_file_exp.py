# -*- coding:utf-8 -*-
# Node-RED 任意文件读取

from VulnScanModel.models import VulnScan
from . import node_red_file_poc


def exp(vuln: VulnScan, cmd, content=""):
    return node_red_file_poc.read_file(vuln.url, cmd)