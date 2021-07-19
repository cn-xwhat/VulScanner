from VulnScanModel.models import VulnScan
from . import inspur_rce_poc


def exp(vuln: VulnScan, cmd, content=""):
    url = vuln.url
    result = inspur_rce_poc.sysShell_rce_test(url, vuln.specify, cmd)
    return result
