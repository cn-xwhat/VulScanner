# -*- coding:utf-8 -*-
# MS17_010

from .. import requestUtil
from ServiceScanModel.models import ServiceScan

def ms17_010_check(ip):
    import binascii, socket
    negotiate_protocol_request = binascii.unhexlify(
        "00000054ff534d42720000000018012800000000000000000000000000002f4b0000c55e003100024c414e4d414e312e3000024c4d312e325830303200024e54204c414e4d414e20312e3000024e54204c4d20302e313200")
    session_setup_request = binascii.unhexlify(
        "00000063ff534d42730000000018012000000000000000000000000000002f4b0000c55e0dff000000dfff02000100000000000000000000000000400000002600002e0057696e646f7773203230303020323139350057696e646f7773203230303020352e3000")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((ip, 445))
        s.send(negotiate_protocol_request)
        s.recv(1024)
        s.send(session_setup_request)
        data = s.recv(1024)
        user_id = data[32:34]
        # Python3 中重新实现了 bytes 和 string 这里需要对原来的 .encode('hex') 重新转换，这里设置为_hex
        ip_hex = bytes(ip, encoding='utf8')
        ip_hex = ''.join(['%02x' % b for b in ip_hex])
        tree_connect_andx_request = "000000%xff534d42750000000018012000000000000000000000000000002f4b%sc55e04ff000000000001001a00005c5c%s5c49504324003f3f3f3f3f00" % (
        (58 + len(ip)), user_id.hex(), ip_hex)
        print(tree_connect_andx_request)
        s.send(binascii.unhexlify(tree_connect_andx_request))
        data = s.recv(1024)
        allid = data[28:36]
        payload = "0000004aff534d422500000000180128000000000000000000000000%s1000000000ffffffff0000000000000000000000004a0000004a0002002300000007005c504950455c00" % allid.hex()
        s.send(binascii.unhexlify(payload))
        data = s.recv(1024)
        s.close()
        if b'\x05\x02\x00\xc0' in data:
            return True  # 存在SMB远程溢出漏洞
        s.close()
        return False
    except:
        return False

def fingerprint(service):
    try:
        if service.port == 445:
            return True
    except:
        return False

def poc(service: ServiceScan):
    try:
        if ms17_010_check(service.ip):
            return ["MS17_010", "SMB远程缓冲区溢出"]
    except:
        return []