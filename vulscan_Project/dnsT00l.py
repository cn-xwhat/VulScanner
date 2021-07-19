from . import requestUtil

cookies = "CNZZDATA1278305074=785399890-1607710109-null%7C1626551643; UM_distinctid=17a162147f1224-0ac81b389aed22-4c3f2d73-151800-17a162147f22f5; PHPSESSID=81d8qnkcc7nt97f3g53u3bi791"

def get_dns_ip():
    resp = requestUtil.get("http://www.dnslog.cn/getdomain.php?t=0.5165514214063338", cookies=cookies)
    return resp.text.strip()

def get_result():
    resp = requestUtil.get("http://www.dnslog.cn/getrecords.php?t=0.5165514214063338", cookies=cookies).json()
    if len(resp) > 0:
        return (resp[0][1], resp[0][2])
    else:
        return False