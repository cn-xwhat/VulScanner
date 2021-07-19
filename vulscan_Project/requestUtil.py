import re
import traceback

import requests
import warnings

from urllib3 import encode_multipart_formdata

warnings.filterwarnings("ignore")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close",
}


def get_cookies(cookie_str):
    cookie_dict = {i.split("=")[0].strip(): i.split("=")[-1].strip() for i in cookie_str.split(";")}
    return cookie_dict


def get(url, cookies="", header=None, timeout=5, session=""):
    f_headers = dict.copy(headers)
    if cookies == "":
        cookies = {}
    else:
        cookies = get_cookies(cookies)
    if header == None:
        header = {}
    f_headers = dict(f_headers, **header)
    try:
        if session == "":
            resp = requests.get(url, cookies=cookies, headers=f_headers, verify=False, timeout=timeout)
        else:
            resp = session.get(url, cookies=cookies, headers=f_headers, verify=False, timeout=timeout)
        if "<meta http-equiv=" in resp.text.lower():
            try:
                if session == "":
                    resp = requests.get(url+"/"+re.findall(r"<meta http-equiv=.*?content=.*?url=(.*?)>", resp.text.lower())[0].replace('"', ""), cookies=cookies, headers=f_headers, verify=False, timeout=timeout)
                else:
                    resp = session.get(url+"/"+re.findall(r"<meta http-equiv=.*?content=.*?url=(.*?)>", resp.text.lower())[0].replace('"', ""), cookies=cookies, headers=f_headers, verify=False, timeout=timeout)
            except:
                pass
        return resp
    except Exception as e:
        traceback.print_exc()
        print(e)
        return None


def post(url, data="", cookies="", header=None, timeout=5, session=""):
    f_headers = dict.copy(headers)
    if cookies == "":
        cookies = {}
    else:
        cookies = get_cookies(cookies)
    if header == None:
        header = {"Content-Type": "application/x-www-form-urlencoded"}
    f_headers = dict(f_headers, **header)
    try:
        if session == "":
            resp = requests.post(url, cookies=cookies, data=data, headers=f_headers, verify=False, timeout=timeout)
        else:
            resp = session.post(url, cookies=cookies, data=data, headers=f_headers, verify=False, timeout=timeout)
        return resp
    except Exception as e:
        traceback.print_exc()
        print(e)
        return None


def get_file_data(filename, filedata, param="file"):  # param: 上传文件的POST参数名
    data = {}
    data[param] = (filename, filedata)  # 名称，读文件
    encode_data = encode_multipart_formdata(data)
    return encode_data
