# -*- coding: utf-8 -*-
import requests

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Connection": "close"
}

def getICP(domain):
    resultDict = {"domain":domain, "unitName": "-", "unitType": "-", "unitICP": "-", "title": "-"}
    try:
        req = requests.get(url=f"https://api.vvhan.com/api/icp?url={domain}", headers=header, timeout=20)
        if req.status_code != 200:
            resultDict["unitName"] = "NtError"
            resultDict["unitType"] = "NtError"
            resultDict["unitICP"] = "NtError"
            resultDict["title"] = "NtError"
            return resultDict
        if len(req.json()) != 2 :
            resultDict["unitName"] = req.json()["info"]["name"]
            resultDict["unitType"] = req.json()["info"]["nature"]
            resultDict["unitICP"] = req.json()["info"]["icp"]
            resultDict["title"] = req.json()["info"]["title"]
        elif req.json()["message"] == "请输入正确的域名":
            resultDict["unitName"] = "DmError"
            resultDict["unitType"] = "DmError"
            resultDict["unitICP"] = "DmError"
            resultDict["title"] = "DmError"
        else:#此域名未备案
            pass
        return resultDict
    except Exception as e:
        resultDict["unitName"] = "NtError"
        resultDict["unitType"] = "NtError"
        resultDict["unitICP"] = "NtError"
        resultDict["title"] = "NtError"
#         print(f"\033[31m[Error] {e}\033[0m")
        pass
    return resultDict