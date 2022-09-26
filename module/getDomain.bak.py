# -*- coding: utf-8 -*-
import re
import tldextract
import requests
requests.packages.urllib3.disable_warnings()

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
#     "Connection": "close"  数据量传输慢 不可立马关闭socket通道
}

def getDomain(ip):
    mainDomainList = []
    domainList = []

    try:
        req1 = requests.get(url=f"http://api.webscan.cc/?action=query&ip={ip}", headers=headers, timeout=20, verify=False)
        if req1.status_code != 200:
            domainList.append("NtError")
            return domainList
        if req1.text != "null":
            jsonData = req1.json()
            for data in jsonData:
                domain = data["domain"]
                if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", domain):
                    #剔除ip
                    continue
                if domain  in mainDomainList:
                    #剔除已有相同主域名
                    continue
                # #domainObj：subdomain='www', domain='baidu', suffix='com'   获取主域名并保存
                domainObj = tldextract.extract(domain)
                mainDomainList.append(f"{domainObj.domain}.{domainObj.suffix}") if f"{domainObj.domain}.{domainObj.suffix}" not in mainDomainList else 0
            domainList=mainDomainList
    except Exception as e:
#         print(f"\033[31m[Error] {e}\033[0m")
        domainList.append("NtError")
        pass
    return domainList

print(getDomain("110.242.68.66"))
print(getDomain("baidu.com"))