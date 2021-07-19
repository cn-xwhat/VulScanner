import configparser
import os
import pymysql

from django.conf import settings
settings.configure()

conf = configparser.ConfigParser()
conf.read(os.getcwd() + "/" + "config.ini")
mysql_config = {  # for mysql and postgresql
        'host': conf.get('global', 'ip'),
        'port': int(conf.get('global', 'port')),
        'user': conf.get('global', 'uname'),
        'password': conf.get('global', 'passwd'),
        'database': conf.get('global', 'table'),
        "connect_timeout": 1
    }

def exec_sql(conn, sql):
    pass

if __name__ == '__main__':
    sql_file = open("poc.sql", "rb")
    try:
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()
        for i in sql_file:
            result = (cursor.execute(i.strip().decode()))
            if not result == 1:
                print("[-]execute sql fail")
                break
        conn.commit()
        conn.close()
        print("[+]install pocs success")
    except Exception as e:
        print("[-]can't connect to mysql")
