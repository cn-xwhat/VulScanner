# -*- coding:utf-8 -*-
# Apache Solr Velocity模板远程执行 

from VulnScanModel.models import VulnScan
from . import apache_solr_velocity_poc


def exp(vuln: VulnScan, cmd, content=""):
    return apache_solr_velocity_poc.rce(vuln.url, vuln.specify, cmd)
