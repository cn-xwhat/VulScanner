import html
import re

from ScanTaskModel.models import ScanTask
from IpModel.models import IpScan
from . import requestUtil

api_url = "https://ip.bmcx.com/?dz="

def get_ips(query, page=0, each_num=0):
    if page == 0:
        ip_list = IpScan.objects.extra(where=[query])
    else:
        ip_list = IpScan.objects.extra(where=[query])[(page - 1) * each_num:page * each_num]
    return ip_list

def get_count(task_id, page=0, each_num=0):  # 获取结果集总数
    try:
        query = "1=1"
        query += " and taskid=%s" % (task_id)
        ip_list = get_ips(query, page, each_num)
        return ip_list.count()
    except:
        return 0

def get_results(task_id, isAll=False, page=0, each_num=0):  # 获取扫描结果，isAll=True获取所有结果，否则获取未显示结果
    result_list = []
    if isAll:
        query = "1=1"
    else:
        query = "isShown=False"
    query += " and taskid=%s" % (task_id)
    ip_list = get_ips(query, page, each_num)
    for i in ip_list:
        result_list.append(i)
        i.isShown = True
        i.save()
    return result_list

def ip_scan(location):
    location = html.escape(location)
    resp = requestUtil.get(api_url + location)
    # print(resp.text)
    results = (re.findall(
        '<td height="25" bgcolor="#FFFFFF" style="text-align: center">(.*?)</td><td bgcolor="#FFFFFF" style="text-align: center">(.*?)</td>',
        resp.text))
    task = ScanTask(ip_range=location, task_count=len(results), mode="ip")
    task.save()
    tid = task.id
    count = 0
    try:
        for i in results:
            count += 1
            ipscan = IpScan(ip=i[0], location=i[1], taskid=tid)
            ipscan.save()
            task.service_process += 1
    finally:
        task.save()
    return True

