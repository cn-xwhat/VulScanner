import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ScanTaskModel.models import ScanTask
from PocModel.models import Poc
from VulnScanModel.models import VulnScan
from ServiceScanModel.models import ServiceScan
from . import serviceUtil, vulnUtil, IpModelUtil

label_dict = {
    "high": "<label class='label label-danger'>{text}</label>",
    "medium": "<label class='label label-primary'>{text}</label>",
    "low": "<label class='label label-success'>{text}</label>",
}

service_row = "<tr><td>{id}</td><td>{ip}</td><td>{port_labels}</td><td>{spec_labels}</td>{note}<td><a href=\"#\"><span class=\"glyphicon glyphicon-eye-{status}\"></span></a></td></tr>"

vuln_label = '''
<label class="label label-{risk}" data-toggle="popover"
                                               data-placement="auto left"
                                               data-content="{desc}"
                                               data-html="true"><a href="javascript:void(0)" onclick="get_exp({id})"">
                                            <span style="color: gainsboro">{port}:</span> {vuln}
                                        </a></label>
'''

service_label = ''' <label class="label label-default" data-toggle="popover"
data-placement="auto right"
data-title="Title: {title}" data-content="Port: {port}<br>Server: {server}"
data-html="true">
<a href="javascript:void(0)" onclick='window.open("{url}")' style="color: white">
<span class='port'>{port}: </span>{t_title}</a></label> '''
note_column = """
<td style="color: crimson" class="text-center note">
    <input class="unactive new-note" value="{note}" id="{ip}" style="height: 22px" name="note"/>
    <span class="note">{note}</span>
</td>
"""

ip_row = """
<tr>
    <td>{id}</td>
    <td id="ip_0">{ip}</td>
    <td id="location" style="color: #2b669a">
        {location}
    </td>
    <td><a href="#"><span class="glyphicon glyphicon-share-alt"></span></a></td>
</tr>
"""


def get_async_result(request: HttpRequest):  # 伪异步，获取实时扫描结果
    mode = request.GET["mode"]
    task_id = request.GET["task_id"]
    task = ScanTask.objects.get(id=task_id)
    count = int(request.GET["count"])
    new_rows = ""
    if mode == "service" or mode == "fofa":
        new_result = serviceUtil.get_results(task_id)
        process = task.service_process / task.task_count
        for i in new_result:
            status = "open" if i["vulnerable"] else "close"
            count += 1
            port_labels = ""
            service_labels = ""
            for p in i["ports"]:
                if not p["title"] == "":
                    service_labels += service_label.format(port=p["port"], title=p["title"], server=p["server"],
                                                           t_title=(
                                                               p["title"][:10] + "..." if len(p["title"]) > 10 else
                                                               p["title"]), url=p["url"])
                port_labels += label_dict[p["type"]].format(text=p["label"]) + " "
            new_rows += service_row.format(id=count, ip=i["ip"], port_labels=port_labels,
                                           spec_labels=service_labels, status=status,
                                           note=note_column.format(note=i["note"], ip=i["ip"]))
    elif mode == "vuln":
        new_result = vulnUtil.get_results(task_id)
        status = "open"
        process = task.vuln_process / task.vuln_count if task.vuln_count != 0 else 0
        for i in new_result:
            count += 1
            service_labels = ""
            vuln_labels = ""
            for p in i["ports"]:
                service_labels += service_label.format(port=p["port"], title=p["title"], server=p["server"],
                                                       t_title=(
                                                           p["title"][:10] + "..." if len(p["title"]) > 10 else
                                                           p["title"]), url=p["url"])
            for v in i["vulns"]:
                vuln_labels += vuln_label.format(risk=v.risk, vuln=v.vulnerability,
                                                 desc=v.description.replace('"', '&quot;'), port=v.port,
                                                 id=v.id)
            new_rows += service_row.format(id=count, ip=i["ip"], port_labels=service_labels,
                                           spec_labels=vuln_labels, status=status, note="")
            # print(new_rows)
    elif mode == "ip":
        count = 0
        new_result = IpModelUtil.get_results(task_id)
        process = task.service_process / task.task_count
        for i in new_result:
            count += 1
            new_rows += ip_row.format(id=count, ip=i.ip, location=i.location)
    return HttpResponse(json.dumps({"html": new_rows, "count": count, "process": process}))


def get_task_id(request: HttpRequest):
    task = ScanTask()
    task.save()
    id = task.id
    task.delete()
    return HttpResponse(id + 1)


def edit(request: HttpRequest):
    id = request.GET["id"]
    mode = request.GET["mode"]
    description = request.GET["description"]
    if mode == "task":
        task = ScanTask.objects.get(id=id)
        task.description = description
        task.save()
    return HttpResponse("success")


def use_poc(request: HttpRequest):
    poc = Poc.objects.get(id=request.GET["id"])
    poc.isUse = not poc.isUse
    poc.save()
    return HttpResponse("success")


def get_exp(request: HttpRequest):
    vuln = VulnScan.objects.get(id=request.GET["id"])
    poc = Poc.objects.get(poc_name=vuln.module)
    cmd = poc.cmd if poc.cmd != "" else "无"
    return HttpResponse(json.dumps([vuln.ip, vuln.vulnerability, cmd]))


def switch_service(request: HttpRequest):
    service_list = ServiceScan.objects.filter(ip=request.GET["ip"], taskid=request.GET["tid"])
    for i in service_list:
        i.vulnerable = not i.vulnerable
        i.save()
    return HttpResponse("success")


def add_note(request: HttpRequest):
    task_id = request.GET["tid"]
    ip = request.GET["ip"]
    note = request.GET["note"]
    service_list = ServiceScan.objects.filter(taskid=task_id, ip=ip)
    for i in service_list:
        i.note = note
        i.save()
    return HttpResponse("success")

def clear_note(request: HttpRequest):
    task_id = request.GET["tid"]
    service_list = ServiceScan.objects.filter(taskid=task_id)
    for i in service_list:
        i.note = ""
        i.vulnerable = False
        i.save()
    return HttpResponse("success")

def switch_poc(request: HttpRequest):
    if request.GET["old"] == "True":
        mode = True
        data = ("禁用所有POC", "glyphicon-ok", "False")
    else:
        mode = False
        data = ("启用所有POC", "glyphicon-remove", "True")
    poc_list = Poc.objects.all()
    for i in poc_list:
        i.isUse = mode
        i.save()
    return HttpResponse(json.dumps([*data]))
