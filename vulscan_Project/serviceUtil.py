import base64
import json
import re

import threading
import socket
import traceback

import requests
import warnings
from ServiceScanModel.models import ServiceScan
from ScanTaskModel.models import ScanTask
from VulnScanModel.models import VulnScan
from . import IpUtil, requestUtil

FOFA_EMAIL = "512147466@qq.com"
FOFA_KEY = "c93af87abe5c61bf106e9d601e15555a"

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

warnings.filterwarnings("ignore")


class Scan(threading.Thread):
    def __init__(self, ip, port, task_id, url=""):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.task_id = task_id
        if self.port in type_dict["high"]:
            self.type = "high"
        elif self.port in type_dict["medium"]:
            self.type = "medium"
        else:
            self.type = "low"
        if not url == "":
            self.url = "http://" + url if not ("https://" in url or "http://" in url) else url
        else:
            self.url = ""

    def run(self):
        service_scan = None
        try:
            if self.url == "":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                s.connect((self.ip, self.port))
                service_scan = ServiceScan(ip=self.ip, port=self.port, taskid=self.task_id, type=self.type)
                if self.port != 443 and self.port != 8443:
                    url = "http://%s:%s" % (self.ip, self.port)
                else:
                    url = "https://%s:%s" % (self.ip, self.port)
            else:
                service_scan = ServiceScan(ip=self.ip, port=self.port, taskid=self.task_id, type=self.type)
                url = self.url
            resp = requestUtil.get(url)
            index = resp.content.find(b'<title>')
            content = resp.content[index:index+100]
            if resp == None:
                raise Exception
            try:
                title = re.findall(r"<title.*?>(.*?)</title>", content.decode("utf-8"), re.DOTALL)[0]
                if title == "":
                    title = "空标题"
            except:
                title = "空标题"
            try:
                server = resp.headers["Server"]
            except:
                server = "None"
            service_scan.title = title
            service_scan.server = server
            service_scan.url = url
        except Exception as e:
            pass
        finally:
            try:
                service_scan.save()
            except:
                pass


def port_scan(ips, port_list, isStart=False, description=""):
    ip_list = IpUtil.get_all_ips(ips)
    if ip_list == []:
        return False
    task = ScanTask(ip_range=ips, task_count=len(ip_list) * len(port_list), isStart=isStart, description=description)
    task.save()
    tid = task.id
    scan_list = []
    for i in ip_list:
        for p in port_list:
            scan_list.append(Scan(i, p, tid))
            if len(scan_list) % 200 == 0:
                for s in scan_list:
                    task.service_process += 1
                    task.save(update_fields=["service_process"])
                    s.start()
                for s in scan_list:
                    s.join()
                scan_list = []
    for s in scan_list:
        task.service_process += 1
        task.save(update_fields=["service_process"])
        s.start()
    for s in scan_list:
        s.join()
    return True

def get_services(query, page=0, each_num=0):
    if page == 0:
        service_list = ServiceScan.objects.extra(where=[query]).values("ip", "vulnerable", "note").distinct()
    else:
        service_list = ServiceScan.objects.extra(where=[query]).values("ip", "vulnerable", "note").distinct()[
                       (page - 1) * each_num:page * each_num]
    return service_list


def get_count(task_id, page=0, each_num=0):    # 获取结果集总数
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
    service_list = get_services(query, page, each_num)
    for i in service_list:
        result = {}
        result["ip"] = i["ip"]
        result["vulnerable"] = i["vulnerable"]
        result["note"] = i["note"]
        query_ip = query + " and ip='%s'" % i['ip']
        result["ports"] = []
        for p in ServiceScan.objects.extra(where=[query_ip]).order_by("type"):
            result["ports"].append({"label": port_label[p.port] if p.port in port_label else "http-%d" % p.port,
                                    "type": p.type, "title": p.title, "server": p.server, "url": p.url,
                                    "port": p.port})
            p.isShown = True
            p.save()
        result_list.append(result)
    return result_list


def delete_task(task_id):
    task = ScanTask.objects.get(id=task_id)
    service_list = ServiceScan.objects.filter(taskid=task_id)
    vuln_list = VulnScan.objects.filter(taskid=task_id)
    task.delete()
    for i in service_list:
        i.delete()
    return True


def fofa_scan(query, isStart=False, description=""):
    print(query)
    if not "country" in query:
        query += ' && country="CN" && region != "HK"'
    b_query = base64.b64encode(query.encode()).decode()
    resp = requestUtil.get(f"https://fofa.so/api/v1/search/all?email={FOFA_EMAIL}&key={FOFA_KEY}&qbase64={b_query}")
    results = (json.loads(resp.text))["results"]
    task = ScanTask(ip_range=query.replace(' && country="CN" && region != "HK"', ''), task_count=len(results), isStart=isStart, mode="fofa", description=description)
    task.save()
    tid = task.id
    scan_list = []
    count = 0
    for i in results:
        count += 1
        scan_list.append(Scan(i[1], i[2], tid, i[0]))
        if len(scan_list) % 5 == 0:
            for s in scan_list:
                task.service_process += 1
                task.save(update_fields=["service_process"])
                s.start()
            for s in scan_list:
                s.join()
            scan_list = []
    for s in scan_list:
        task.service_process += 1
        task.save(update_fields=["service_process"])
        s.start()
    for s in scan_list:
        s.join()
    return True
