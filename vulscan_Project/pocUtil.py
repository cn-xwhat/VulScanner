import threading

from django.http import HttpRequest

import PocModel.models
from . import fileUtil


class Poc(threading.Thread):

    def __init__(self, module, service, risk):
        threading.Thread.__init__(self)
        self.module = module
        self.service = service
        self.risk = risk
        self.result = []
        self.specify = ""

    def run(self):
        module = __import__("vulscan_Project.modules.%s_poc" % self.module, fromlist=self.module)
        fingerprint = getattr(module, "fingerprint")
        poc = getattr(module, "poc")
        try:
            fingerprint_result = fingerprint(self.service)
            if fingerprint_result:  # 指纹检测，如满足特征则进行漏洞扫描
                if not type(fingerprint_result) == bool:
                    self.service.speciality = fingerprint_result
                self.result = poc(self.service)
                if type(self.result) == tuple:
                    self.specify = self.result[1]
                    self.result = self.result[0]
                else:
                    self.result = self.result
                if not type(self.result) == list:
                    self.result = []
                elif len(self.result) > 1:
                    if len(self.result) == 2:
                        self.result.append(self.risk)
                    self.result.append(self.module)
                    self.result.append(self.specify)
            else:
                self.result = []
        except:
            self.result = []

    def get_result(self):
        return self.result
