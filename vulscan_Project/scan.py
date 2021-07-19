import codecs
import re
import traceback

from django.http import HttpRequest, HttpResponse, FileResponse
from django.shortcuts import render

from ScanTaskModel.models import ScanTask
from ServiceScanModel.models import ServiceScan
from VulnScanModel.models import VulnScan

from . import serviceUtil, pageUtil, fileUtil, vulnUtil, pocUtil, pocModelUtil, ExpUtil, IpModelUtil

port_dict = {
    "0": [22, 23, 3389, 80, 443, 8080, 8081, 7001, 3306, 1433, 1521, 6379, 2375, 5432, 8443],
    "1": [80, 81, 8080, 8081, 3306, 1433, 5432],
    "2": [i for i in range(1, 65535)]
}

port_label = {
    1433: "mssql-1433",
    3306: "mysql-3306",
    5432: "postgresql-5432",
    6379: "redis-6379",
    443: "https-443",
}

poc_type_list = pocModelUtil.poc_type_list

def get_ctx(ctx, showmenu, query="1=1", mode=""):
    ctx["showmenu"] = showmenu
    # task_list = ScanTask.objects.all().extra(where=[query])
    task_list = ScanTask.objects.all().filter(mode="" if (mode == 'service' or mode == "vuln") else mode).extra(where=[query])
    if mode == "service":
        ports = []
        for p in port_dict.values():
            ports.append([str(i) for i in p])
        ctx["ports"] = [",".join(i) for i in ports]
    ctx["task_list"] = task_list
    ctx["mode"] = mode
    return ctx


def scan(request: HttpRequest, mode, query):
    ctx = get_ctx({}, False, query, mode)
    each_num = 100
    if "page" in request.GET:
        page = int(request.GET['page'])
    else:
        page = 1
    try:
        if not "id" in request.GET:
            task = ctx["task_list"].last()
            task_id = task.id
        else:
            task_id = request.GET["id"]
            task = ScanTask.objects.get(id=task_id)
        if mode == "service" or mode == "fofa":
            ctx["process"] = task.service_process / task.task_count * 100 if not task.task_count == 0 else 0
            count = serviceUtil.get_count(task_id)
            ctx["count"] = serviceUtil.get_count(task_id, page=page, each_num=each_num)
            result_list = serviceUtil.get_results(task_id, isAll=True, page=page, each_num=each_num)
        elif mode == "vuln":
            ctx["process"] = task.vuln_process / task.vuln_count * 100 if not task.vuln_count == 0 else 0
            ctx["poc_type_list"] = poc_type_list
            count = vulnUtil.get_count(task_id)
            ctx["count"] = vulnUtil.get_count(task_id, page=page, each_num=each_num)
            result_list = vulnUtil.get_results(task_id, isAll=True, page=page, each_num=each_num)
        elif mode == "ip":
            ctx["process"] = task.service_process / task.task_count * 100 if not task.task_count == 0 else 0
            count = IpModelUtil.get_count(task_id)
            ctx["count"] = IpModelUtil.get_count(task_id, page=page, each_num=each_num)
            result_list = IpModelUtil.get_results(task_id, isAll=True, page=page, each_num=each_num)
        ctx["task"] = task
        ctx["isPause"] = task.isPause
    except:
        traceback.print_exc()
        result_list = []
        count = 0
        ctx["count"] = 0
        ctx["task_id"] = 0
    finally:
        if "new_ip" in request.GET:
            ctx["new_ip"] = request.GET["new_ip"]
        if "new_query" in request.GET:
            ctx["new_ip"] = request.GET["new_query"]
        if "desc" in request.GET:
            ctx["description"] = request.GET["desc"]
        if "port" in request.GET:
            ctx["port"] = request.GET["port"]
        else:
            ctx["port"] = 0
        if "type" in request.GET:
            ctx["type"] = request.GET["type"]
        else:
            ctx["type"] = 0
        if "port2" in request.GET:
            ctx["port2"] = request.GET["port2"]
    last_page = pageUtil.get_lastpage(count, each_num)
    ctx = pageUtil.get_ctx(ctx, "result_list", result_list, page, last_page,
                           "扫描", request.get_full_path())
    return render(request, "%s_scan.html" % mode, ctx)


def service_scan(request: HttpRequest):
    return scan(request, "service", "1=1")


def vuln_scan(request: HttpRequest):
    return scan(request, "vuln", "vuln_process>0")


def start_scan(request: HttpRequest):
    if request.method == "GET":
        mode = request.GET["mode"]
        if mode == 'service':
            print(request.GET)
            if "start" in request.GET and request.GET["start"] == "true":
                isStart = True
            else:
                isStart = False
            ips = request.GET["ips"].strip()
            port_list = port_dict[request.GET["port"]] if request.GET["port"] != '3' else request.GET["port2"].split(",")
            port_list = [int(i) for i in port_list]
            description = request.GET["description"]
            if not serviceUtil.port_scan(ips, port_list, isStart, description):
                return HttpResponse("fail")
        elif mode == "vuln":
            task_id = request.GET["id"]
            vuln_type = request.GET["type"]  # 后期添加漏洞库支持，根据vuln_type获取扫描漏洞类型
            print(vuln_type)
            if not vulnUtil.vuln_scan(task_id, int(vuln_type)):
                return HttpResponse("fail")
        elif mode == "fofa":
            query = request.GET["ips"]
            description = request.GET["description"]
            if not serviceUtil.fofa_scan(query, False, description):
                return HttpResponse("fail")
        elif mode == "ip":
            query = request.GET["location"].strip()
            if not IpModelUtil.ip_scan(query):
                return HttpResponse("fail")
        return HttpResponse("success")


def get_query(request: HttpRequest):  # 过滤任务
    query = "1=1"
    if "ip" in request.GET:
        query += r" and ip_range LIKE '%%{}%%'".format(request.GET["ip"])
    if "service" in request.GET:
        if request.GET["service"] == "1":
            query += " and service_process = task_count"
        else:
            query += " and not service_process = task_count"
    if "vuln" in request.GET:
        if request.GET["vuln"] == "1":
            query += " and vuln_process = vuln_count and not vuln_count = 0"
        else:
            query += " and not vuln_process = vuln_count or vuln_count = 0"
    return query


def task_list(request: HttpRequest, mode="service"):  # 获取任务列表
    if mode == "ip":
        page_file = "ip_list.html"
    else:
        page_file = "task_list.html"
    query = get_query(request)
    ctx = get_ctx({}, True, query, mode)
    each_num = 20  # 每页显示行数
    page = 1
    if "page" in request.GET:
        page = int(request.GET["page"])
    task_list = ctx["task_list"]
    last_page = pageUtil.get_lastpage(task_list.count(), each_num)
    ctx = pageUtil.get_ctx(ctx, "task_list", task_list[(page - 1) * each_num:page * each_num], page, last_page,
                           "任务", request.get_full_path())
    return render(request, page_file, ctx)


def fofa_list(request: HttpResponse):  # 获取fofa采集结果列表
    return task_list(request, "fofa")

def export_file(request: HttpRequest):
    data = fileUtil.export_file(request.GET["id"], request.GET["mode"])
    resp = HttpResponse(data)
    resp.write(codecs.BOM_UTF8)
    resp["content-type"] = "text/csv;charset=utf-8"
    resp["Content-Disposition"] = "attachment; filename=%s_%s.csv" % (request.GET["id"], request.GET["mode"])
    return resp


def delete_task(request: HttpRequest):
    if serviceUtil.delete_task(request.GET["id"]):
        return HttpResponse("success")


def stop_task(request: HttpRequest):
    task = ScanTask.objects.get(id=request.GET["id"])
    task.isPause = not task.isPause
    task.save()
    return HttpResponse("success")


def repeat_scan(request: HttpRequest):
    task_id = request.GET["id"]
    task = ScanTask.objects.get(id=task_id)
    vuln_list = VulnScan.objects.filter(taskid=task_id)
    task.vuln_count = task.vuln_process = 0
    task.isPause = False
    task.save()
    for i in vuln_list:
        i.delete()
    return HttpResponse("success")


def fofa_scan(request: HttpRequest):
    return scan(request, "fofa", "mode='fofa'")


def get_poc_ctx(ctx, type=""):
    all_down = True
    ctx["showmenu"] = False
    ctx["poc_list"] = pocModelUtil.get_pocs(type)
    for i in ctx["poc_list"]:
        if i.isUse:
            all_down = False
            break
    ctx["all_down"] = all_down
    ctx["mode"] = "poc"
    ctx["risk_dict"] = {
        "danger": "高危",
        "warning": "中危",
        "success": "低危"
    }
    ctx["type"] = poc_type_list
    return ctx


def poc_list(request: HttpRequest):
    if "type" in request.GET:
        if request.GET["type"] == "-1":
            type = "其他"
        else:
            type = poc_type_list[int(request.GET["type"])-1]
    else:
        type = ""
    ctx = get_poc_ctx({}, type)
    each_num = 20  # 每页显示行数
    page = 1
    if "page" in request.GET:
        page = int(request.GET["page"])
    poc_list = ctx["poc_list"]
    last_page = pageUtil.get_lastpage(poc_list.count(), each_num)
    ctx = pageUtil.get_ctx(ctx, "poc_list", poc_list[(page - 1) * each_num:page * each_num], page, last_page,
                           "POC", request.get_full_path())
    return render(request, "poc_list.html", ctx)


def add_poc(request: HttpRequest):
    pocModelUtil.add_poc(request)
    return HttpResponse("success")

def exp(request: HttpRequest):
    return HttpResponse(ExpUtil.exp(request))

def ip_scan(request: HttpRequest):
    return scan(request, "ip", "1=1")


def ip_list(request: HttpRequest):
    return task_list(request, "ip")