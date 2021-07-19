from django.http import HttpRequest

from PocModel.models import Poc
from . import fileUtil

poc_type_list = ["命令执行", "弱密码", "任意文件上传", "SQL注入", "SSRF", "任意文件读取", "垂直越权", ]
risk_list = ["danger", "warning", "success"]
cmd_list = ["执行命令", "上传文件", "读取文件"]


def get_pocs(type="", q=""):
    query = "1=1"
    if not type == "":
        query += " and type='%s'" % type
    if not q == "":
        query += " and " + q
    poc_list = Poc.objects.order_by("type").extra(where=[query]).order_by("risk", "type")
    return poc_list


def add_poc(request: HttpRequest):
    poc = Poc(real_name=request.GET["real_name"], poc_name=request.GET["poc_name"], hasExp=request.GET["hasExp"],
              type=poc_type_list[int(request.GET["type"])], risk=risk_list[int(request.GET["risk"])])
    poc_temp_file = fileUtil.open_file("poc_temp.txt", "rb", "temp")
    exp_temp_file = fileUtil.open_file("exp_temp.txt", "rb", "temp")
    poc_file = fileUtil.open_file(request.GET["poc_name"] + "_poc.py", "wb", "modules")
    poc_file.write(b"# -*- coding:utf-8 -*-\n")
    poc_file.write(("# " + request.GET["real_name"] + "\n").encode("UTF-8"))
    poc_file.write(poc_temp_file.read().replace(b"{vuln}", str(request.GET["real_name"]).encode()))
    poc_file.close()
    poc_temp_file.close()
    if request.GET["hasExp"] != '0':
        exp_file = fileUtil.open_file(request.GET["poc_name"] + "_exp.py", "wb", "modules")
        exp_file.write(b"# -*- coding:utf-8 -*-\n")
        exp_file.write(("# " + request.GET["real_name"] + "\n").encode("UTF-8"))
        exp_file.write(exp_temp_file.read().replace(b'{poc}', ('%s_poc' % (request.GET["poc_name"])).encode()))
        exp_file.close()
        poc.cmd = cmd_list[int(request.GET["cmd"])]
    poc.save()
