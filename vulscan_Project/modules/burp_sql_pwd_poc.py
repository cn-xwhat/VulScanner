import asyncio
import time

import pymysql
import psycopg2
import pymssql
import redis
import threading

from aiomysql import connect

from .. import fileUtil

modules = {
    3306: "mysql",
    1433: "mssql",
    6379: "redis",
    5432: "postgresql",
}

class Sql_Config():
    mysql_config = {  # for mysql and postgresql
        'host': "",
        'port': 3306,
        'user': '',
        'password': '',
        "connect_timeout": 0.5
    }

    postgresql_config = {
        'host': "",
        'port': 5432,
        'user': '',
        'password': '',
        "connect_timeout": 0.5
    }

    mssql_config = {  # for mssql
        "server": "",
        "port": 1433,
        "user": "",
        "password": "",
        "database": "master",
        "login_timeout": 0.5
    }

    redis_config = {
        "host": "",
        "port": 6379,
        "password": "",
        "socket_connect_timeout": 1
    }


class SqlBurp(threading.Thread):
    def __init__(self, ip, port, module, user, password):
        threading.Thread.__init__(self)
        self.module = module
        self.config = dict.copy(getattr(Sql_Config, module + "_config"))
        self.config["host"] = ip
        self.config["port"] = port
        if "user" in self.config:
            self.config["user"] = user
        self.config["password"] = password
        self.result = False
        self.loop = asyncio.new_event_loop()

    async def mysql_burp(self):
        try:
            await asyncio.wait_for(connect(**self.config), 0.5)
        except Exception as e:
            raise Exception

    def mssql_burp(self):
        try:
            conn = pymssql.connect(**self.config)
            return True
        except:
            return False

    def redis_burp(self):
        try:
            pool = redis.ConnectionPool(**self.config)
            r = redis.Redis(connection_pool=pool)
            r.execute_command("PING")
            return True
        except Exception as e:
            return False

    def postgresql_burp(self):
        try:
            conn = psycopg2.connect(**self.config)
            return True
        except Exception as e:
            return False

    def run(self):
        burp_func = getattr(self, self.module + "_burp")
        if not self.module == "mysql":
            if burp_func():
                # user = self.config["user"] if "user" in self.config else ""
                self.result = True
        else:
            # print("mysql")
            try:
                self.loop.run_until_complete(self.mysql_burp())
                self.result = True
            except Exception as e:
                self.result = False
        self.loop.close()


    def get_result(self):
        return self.result


def sql_pwd_burp(ip, port):
    if port in modules:
        module = modules[port]
    else:
        return []
    with fileUtil.open_file(f"dict_{module}/dic_username_{module}.txt", "r") as user_file:
        with fileUtil.open_file(f"dict_{module}/dic_password_{module}.txt", "r") as pwd_file:
            username = [i.strip() for i in user_file.read().split("\n")]
            password = [i.strip() for i in pwd_file.read().split("\n")]
    burp_list = []
    for u in username:
        for p in password:
            burp = SqlBurp(ip, port, module, u, p)
            burp_list.append(burp)
            if len(burp_list) % 10 == 0:
                for b in burp_list:
                    b.start()
                for b in burp_list:
                    b.join()
                for b in burp_list:
                    if b.get_result() == True:
                        return ["%s弱密码" % module, "用户名：%s<br>密码：%s" % (b.config["user"] if "user" in b.config else "", b.config["password"])]
                burp_list = []
    for b in burp_list:
        b.start()
    for b in burp_list:
        b.join()
    for b in burp_list:
        if b.get_result() == True:
            return ["%s弱密码" % module, "用户名：%s<br>密码：%s" % (b.config["user"] if "user" in b.config else "", b.config["password"])]
    return []


def fingerprint(service):
    if service.port in modules:
        return True


def poc(service):  # 传递vuln_scan的任务，字典键(ip,port)，为方便批量执行，每个poc文件的主函数都为poc(ip, port, url)
    try:
        result = sql_pwd_burp(service.ip, service.port)
    except Exception as e:
        result = []
    return result
