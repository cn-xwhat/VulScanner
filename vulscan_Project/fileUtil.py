import os

from ScanTaskModel.models import ScanTask
from ServiceScanModel.models import ServiceScan
from VulnScanModel.models import VulnScan
from IpModel.models import IpScan



def export_file(task_id, mode):
    csv_data = ""
    if mode == "service":
        data_list = ServiceScan.objects.filter(taskid=task_id)
        field_names = [i.name for i in ServiceScan._meta.fields]
    elif mode == "vuln":
        data_list = VulnScan.objects.filter(taskid=task_id)
        field_names = [i.name for i in VulnScan._meta.fields]
    else:
        data_list = IpScan.objects.filter(taskid=task_id)
        field_names = [i.name for i in IpScan._meta.fields]
    csv_data += ",".join(field_names) + "\n"
    for i in data_list:
        data = []
        for j in field_names:
            data.append(str(getattr(i, j)))
        csv_data += ",".join(data) + "\n"
    return csv_data.encode("utf-8")


def open_file(filename, mode="r", dir="dict"):
    return open(os.getcwd() + "/vulscan_Project/%s/%s"%(dir, filename), mode)

def get_burp_list(module):
    user_file = open_file(f"dict_{module}/dic_username_{module}.txt", "r")
    pwd_file = open_file(f"dict_{module}/dic_password_{module}.txt", "r")
    burp_list = []
    user_list = [i.strip() for i in user_file.readlines()]
    pwd_list = [i.strip() for i in pwd_file.readlines()]
    for u in user_list:
        for p in pwd_list:
            if not u == "" and not p == "":
                burp_list.append((u.strip(),p.strip()))
    return burp_list