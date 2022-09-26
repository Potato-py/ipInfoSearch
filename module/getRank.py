import re
import requests

headers = {
    "Referer": "https://www.aizhan.com/cha/",
    "Host": "www.aizhan.com",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
#     "Connection": "close"
}

def getRank(domain):
    url = f"https://www.aizhan.com/cha/{domain}/"#f"https://seo.chinaz.com/{domain}"
    rankDict = {"baiduRank": 0, "yidongRank": 0, "360Rank": 0, "sougouRank": 0, "googleRank": 0}
    try:
        req = requests.get(url, headers=headers, timeout=20)
        if req.status_code != 200:
            rankDict["baiduRank"] = "NtError"
            rankDict["yidongRank"] = "NtError"
            rankDict["360Rank"] = "NtError"
            rankDict["sougouRank"] = "NtError"
            rankDict["googleRank"] = "NtError"
            return rankDict
        # 正则匹配爬虫权重特征
        baiduRank = re.compile(r'aizhan.com/images/br/(.*?).png')
        yidongRank = re.compile(r'aizhan.com/images/mbr/(.*?).png')
        _360Rank = re.compile(r'aizhan.com/images/360/(.*?).png')
        sougouRank = re.compile(r'aizhan.com/images/sr/(.*?).png')
        googleRank = re.compile(r'aizhan.com/images/pr/(.*?).png')
        try:
            rankDict["baiduRank"] = int(baiduRank.findall(req.text)[0])
            rankDict["yidongRank"] = int(yidongRank.findall(req.text)[0])
            rankDict["360Rank"] = int(_360Rank.findall(req.text)[0])
            rankDict["sougouRank"] = int(sougouRank.findall(req.text)[0])
            rankDict["googleRank"] = int(googleRank.findall(req.text)[0])
        except Exception as e:
#             print(f"\033[31m[Error] {e}\033[0m")
            pass
    except Exception as e:
        rankDict["baiduRank"] = "NtError"
        rankDict["yidongRank"] = "NtError"
        rankDict["360Rank"] = "NtError"
        rankDict["sougouRank"] = "NtError"
        rankDict["googleRank"] = "NtError"
#         print(f"\033[31m[Error] {e}\033[0m")
        pass
    return rankDict