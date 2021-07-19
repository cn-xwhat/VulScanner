# -*- coding:utf-8 -*-
# ShowDoc 任意文件上传

from . import showdoc_poc

from VulnScanModel.models import VulnScan


def exp(vuln: VulnScan, cmd, content=""):
    result = showdoc_poc.showdoc_poc(vuln.url, cmd, content, "exp")
    return "上传成功，shell地址：\n%s" % result
