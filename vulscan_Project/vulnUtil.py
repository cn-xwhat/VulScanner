import re

import threading
import socket
import requests
from ServiceScanModel.models import ServiceScan
from ScanTaskModel.models import ScanTask
from VulnScanModel.models import VulnScan
from . import IpUtil, pocUtil, pocModelUtil
from html.parser import HTMLParser

port_label = {
    1433: "mssql-1433",
    3306: "mysql-3306",
    5432: "postgresql-5432",
    6379: "redis-6379",
    443: "https-443",
    2375: "docker-2375",
    22: "ssh-22",
    23: "telnet-23",
    1521: "oracle-1521",
    3389: "rdp-3389"
}

type_dict = {
    "high": [2375, 1099, 3389, 22],
    "medium": [1433, 1521, 3306, 5432, 6379]
}

poc_type_list = pocModelUtil.poc_type_list

def get_services(query, page=0, each_num=0):
    if page == 0:
        service_list = VulnScan.objects.extra(where=[query]).values("ip").distinct()
    else:
        service_list = VulnScan.objects.extra(where=[query]).values("ip").distinct()[
                       (page - 1) * each_num:page * each_num]
    return service_list


def get_count(task_id, page=0, each_num=0):  # 获取结果集总数
    query = "1=1"
    query += " and taskid=%s" % (task_id)
    service_list = get_services(query, page, each_num)
    return service_list.count()


def get_results(task_id, isAll=False, page=0, each_num=0):  # 获取扫描结果，isAll=True获取所有结果，否则获取未显示结果
    result_list = []
    if isAll:
        query = "1=1"
    else:
        query = "isShown=False"
    query += " and taskid=%s" % (task_id)
    vuln_list = get_services(query, page, each_num)
    for i in vuln_list:
        result = {}
        result["ip"] = i["ip"]
        query_ip = query + " and ip='%s'" % i['ip']
        result["ports"] = []
        result["vulns"] = []
        for v in VulnScan.objects.extra(where=[query_ip]):
            result["vulns"].append(v)
            v.isShown = True
            v.save()
        for p in ServiceScan.objects.extra(where=[query_ip.replace("isShown=False", "1=1")+"and url!=''"]).order_by("type"):
            result["ports"].append({"label": port_label[p.port] if p.port in port_label else "http-%d" % p.port,
                                    "type": p.type, "title": p.title, "server": p.server, "url": p.url,
                                    "port": p.port})
        result_list.append(result)
    return result_list


def vuln_scan(task_id, vuln_type=0):
    q = "isUse=1"
    if vuln_type > 0:
        q += "& type = %s"%poc_type_list[vuln_type]
    print(q)
    try:
        poc_module_list = [(i.poc_name, i.risk, i.poc_name) for i in pocModelUtil.get_pocs(q=q)]
    except:
        poc_module_list = [(i.poc_name, i.risk, i.poc_name) for i in pocModelUtil.get_pocs(q="id=2")]
    print(poc_module_list)
    # print(poc_module_list)
    task = ScanTask.objects.get(id=task_id)
    task.isStart = True
    task.save()

    def poc():
        for p in poc_list:
            task.vuln_process += 1
            task.save(update_fields=["vuln_process"])
            p.start()
        for p in poc_list:
            p.join()
        for p in poc_list:
            result = p.get_result()
            if not result == [] and type(result) == list:
                vulnscan = VulnScan(taskid=task_id, ip=p.service.ip, port=p.service.port, url=p.service.url,
                                    vulnerability=result[0],
                                    description=result[1][:200], risk=result[2], module=result[3], specify=result[4])
                service_list = ServiceScan.objects.filter(ip=p.service.ip, taskid=task_id)
                for i in service_list:
                    i.vulnerable = True
                    if not vulnscan.vulnerability in i.note:
                        i.note = ", ".join([i.note, vulnscan.vulnerability]).strip(", ")
                    i.save()
                vulnscan.save()

    if int(vuln_type) == 0:
        poc_count = len(poc_module_list)
    else:
        poc_count = len(poc_module_list)
    task_list = [i for i in ServiceScan.objects.filter(taskid=task_id)]
    task.vuln_count = poc_count * len(task_list)
    task.save(update_fields=["vuln_count"])
    poc_list = []
    count = 0
    for i in task_list:
        count += 1
        # print("%s:%s"%(i.ip, i.port))
        for m in poc_module_list:
            # 封装入pocUtil中，可多线程并发，入口函数为poc(module, ip, port, url)
            poc_list.append(pocUtil.Poc(m[0], i, m[1]))
            if len(poc_list) % 1 == 0:
                poc()
                poc_list = []
    poc()
    return True
