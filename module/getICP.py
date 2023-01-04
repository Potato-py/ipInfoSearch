# -*- coding: utf-8 -*-
from lxml import etree
import requests
import socket
import re
import tldextract
requests.packages.urllib3.disable_warnings()

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Connection": "close"
}

def getICP(domain,replayNun=0):
    resultDict = {"domain":domain, "unitName": "-", "unitType": "-", "unitICP": "-", "title": "-"}
    try:
        req = requests.get(url=f"https://icplishi.com/{domain}", headers=header, timeout=20)
        if req.status_code!=200 and replayNun < 2:
            replayNun += 1
            return getICP(domain,replayNun)
        if req.status_code != 200 and replayNun == 2:
            resultDict = {"domain":domain, "unitName": f"NtError:Code{req.status_code}", "unitType": "NtError", "unitICP": "NtError", "title": "NtError"}
            return resultDict
        html=etree.HTML(req.text,etree.HTMLParser())
        SpanTag = html.xpath('//div[@class="module mod-panel"]/div[@class="bd"]/div[@class="box"]/div[@class="c-bd"]/table/tbody/tr/td/span/text()')
        ATag = html.xpath('//div[@class="module mod-panel"]/div[@class="bd"]/div[@class="box"]/div[@class="c-bd"]/table/tbody/tr/td/a/text()')
        token = html.xpath('//div[@id="J_beian"]/@data-token')
        if len(ATag)>=2 and len(SpanTag)>=2 and (SpanTag[1] != "未备案"):
            resultDict = {"domain":domain, "unitName": ATag[0], "unitType": SpanTag[1], "unitICP": ATag[1], "title": SpanTag[0]}
        if (token and resultDict["unitName"]=="-" ) or (token and "ICP" not in resultDict["unitICP"]) or (token and '-' in SpanTag[1]):
            resultDict = getIcpFromToken(domain,token[0])
    except Exception as e:
        resultDict = {"domain":domain, "unitName": "NtError", "unitType": "NtError", "unitICP": "NtError", "title": "NtError"}
#         print(f"\033[31m[Error] func1 code:{req.status_code} {e}\033[0m")
        pass
#     print(req.text)
#     print(SpanTag)
#     print(ATag)
    return resultDict
# print(getICP("potato.gold"))

#两次出现"msg"="等待结果"，为未查询出结果
def getIcpFromToken(domain,token,replayNun=0):
    try:
        req = requests.get(f"https://icplishi.com/query.do?domain={domain}&token={token}", headers=header, timeout=20)
#         print(req.text)
#         print(req.status_code)
#         print(f"https://icplishi.com/query.do?domain={domain}&token={token}")
        if (req.status_code!=200 or req.json()["msg"]=="等待结果") and replayNun < 2:
            replayNun += 1
            return getIcpFromToken(domain,token,replayNun)
        data = req.json()["data"]
        if req.status_code!=200 or req.json()["msg"]=="等待结果" or len(data)==0 or len(data[0])==0 or data[0]["license"]== "未备案":
            resultDict = {"domain":domain, "unitName": "-", "unitType": "-", "unitICP": "-", "title": "-"}
        else:
            resultDict = {"domain":domain, "unitName": data[0]["company"], "unitType": data[0]["character"], "unitICP": data[0]["license"], "title": data[0]["home_site"]}
    except Exception as e:
        resultDict = {"domain":domain, "unitName": "NtError", "unitType": "NtError", "unitICP": "NtError", "title": "NtError"}
#         print(f"\033[31m[Error] func2 code:{req.status_code} msg:{e}\033[0m")
        pass
    return resultDict