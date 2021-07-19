# -*- coding:utf-8 -*-
# Apache Flink 任意文件读取

from VulnScanModel.models import VulnScan
from . import apache_flink_file_poc


def exp(vuln: VulnScan, cmd, content=""):
    return apache_flink_file_poc.flink_file_poc(vuln.url, cmd, "exp")