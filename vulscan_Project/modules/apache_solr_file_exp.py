# -*- coding:utf-8 -*-
# Apache Solr 任意文件读取

from VulnScanModel.models import VulnScan
from . import apache_solr_file_poc


def exp(vuln: VulnScan, cmd, content=""):
    return apache_solr_file_poc.solr_file_poc(vuln.url, vuln.specify, cmd, "exp")
