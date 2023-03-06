# -*- coding: utf-8 -*-
# author Potato
# date 2022-09-26 09:57:02

import os
import sys
import re
import string
import requests
requests.packages.urllib3.disable_warnings()
import csv
import time
import argparse
import tldextract

from module.font import *
from module.getDomain import getDomain
from module.getRank import getRank
from module.getICP import getICP

def printTime():
    return f"[{blue(time.strftime('%H:%M:%S', time.localtime()))}] - "

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", dest="target", required=False, type=str, help="目标IP/域名")
    parser.add_argument("-f", dest="file", required=False, type=str, default="", help=f"包含目标IP/域名的文件")
    parser.add_argument("-r", dest="rank", required=False, type=int, default=0, help="展示权重不小于R的数据 (默认0)")
    parser.add_argument("-rt", dest="rankTarget", required=False, type=int, default=0, help="展示权重[0所有][1百度][2移动][3三六零][4搜狗][5谷歌] (默认0所有)")
    parser.add_argument('-showE', dest="showDominError", required=False, action="store_true", default=False, help="展示反查域名网络错误信息 (默认关闭)")
    parser.add_argument('-icp', dest="icp", required=False, action="store_true", default=False, help="查询ICP备案信息 (默认关闭)")
    parser.add_argument("-o", dest="output", required=False, type=str, default=f"{fistDate}", help=f"输出文件 (默认输出 ./Result/{fistDate}.csv)")
    argsObj = parser.parse_args()
    if not argsObj.target and not argsObj.file:
        print(red('\n[x] 用法:python ipInfoSearch.py [-t 目标IP/域名] [-f 含多个目标的文件] [-r 权重最小值] [-icp 备案查询] [-o 输出文件]\n\n[-] 举例:python ipInfoSearch.py -t 127.0.0.1 -r 1 -icp '))
        sys.exit()
    if argsObj.file:
        if not os.path.isfile(argsObj.file):
            print(printTime()+f"\033[31m[Error] 加载文件[{argsObj.file}]失败\033[0m")
            sys.exit()
    print(printTime()+bold(f"[Info] -t    ：  {argsObj.target}"))
    print(printTime()+bold(f"[Info] -f    ：  {argsObj.file}"))
    print(printTime()+bold(f"[Info] -r    ：  {argsObj.rank}"))
    print(printTime()+bold(f"[Info] -rt   ：  {argsObj.rankTarget}"))
    print(printTime()+bold(f"[Info] -showE：  {argsObj.showDominError}"))
    print(printTime()+bold(f"[Info] -icp  ：  {argsObj.icp}"))
    print(printTime()+bold(f"[Info] -o    ：  ./Result/{argsObj.output}.vsv"))
    return argsObj

# 解析输入目标数据
def parseData(data):
    domainObj = tldextract.extract(data)
    #domainObj：subdomain='www', domain='baidu', suffix='com'
    #判断是否为域名
    if not domainObj.suffix:
        #判断是否为IP
        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",domainObj.domain):
            return f"{domainObj.domain}"
        else:#既不是域名也不是ip
            return ""
    else:
        return f"{domainObj.domain}.{domainObj.suffix}"

# 加载目标IP/域名
def loadTarget(file, target):
    targetList = []
    if file:
        f = open(file, encoding="utf8")
        for line in f.readlines():
            targetData = parseData(line.strip())
            if targetData and targetData not in targetList:
                targetList.append(targetData)
        f.close()

    if target:
        targetData = parseData(target.strip())
        if targetData and targetData not in targetList:
            targetList.append(targetData)

    return targetList

def rtDel(list):
    if args.rankTarget==1:
        del list[3],list[3],list[3],list[3]
    elif args.rankTarget==2:
        del list[2],list[3],list[3],list[3]
    elif args.rankTarget==3:
        del list[2],list[2],list[3],list[3]
    elif args.rankTarget==4:
        del list[2],list[2],list[2],list[3]
    elif args.rankTarget==5:
        del list[2],list[2],list[2],list[2]
    return list

def getIpInfo(target):

    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", target):
        #如果目标是IP格式，获取域名
        domainList = getDomain(target)
    else:
        #目标为域名格式，直接赋值
        domainList = [target]

    #获取权重，任意一项满足即可
    for domain in domainList:
        #反查域名存在问题的单独处理
        if domain == "NtError" and args.showDominError:
            result = [target, domain,'-','-','-','-','-','-','-','-']
            tableDataList=[
                [result[0], 17],
                [result[1], 20],
                [result[2], 10],
                [result[3], 10],
                [result[4], 10],
                [result[5], 10],
                [result[6], 10],
                [result[7], 37],
                [result[8], 10],
                [result[9], 22]
            ]
            if not args.icp:
                del tableDataList[-1],tableDataList[-1],tableDataList[-1]
            printT(rtDel(tableDataList))
            csvWriter.writerow(result)

            if domain != list(domainList)[-1] or target != targetList[-1]:
                printT(rtDel([17,20,10,10,10,10,10,37,10,22]),"middle") if args.icp else printT(rtDel([17,20,10,10,10,10,10]),"middle")
            else:
                printT(rtDel([17,20,10,10,10,10,10,37,10,22]),"bottom") if args.icp else printT(rtDel([17,20,10,10,10,10,10]),"middle")

            break

        rankDict = getRank(domain)
        for rankKey in rankDict:
            if (isinstance(rankDict[rankKey],str) and "Error" in rankDict[rankKey]) or (isinstance(rankDict[rankKey],int) and rankDict[rankKey] >= args.rank): #大于等于制定rank值 或 网络请求失败
                if args.icp:
                    icpResult = getICP(domain)
                    result = [target, domain, rankDict["baiduRank"], rankDict["yidongRank"], rankDict["360Rank"], rankDict["sougouRank"],rankDict["googleRank"],icpResult["unitName"], icpResult["unitType"], icpResult["unitICP"] ]
                    tableDataList=[
                        [result[0], 17],
                        [result[1], 20],
                        [result[2], 10],
                        [result[3], 10],
                        [result[4], 10],
                        [result[5], 10],
                        [result[6], 10],
                        [result[7], 37],
                        [result[8], 10],
                        [result[9], 22]
                    ]
                    printT(rtDel(tableDataList))
                    csvWriter.writerow(result)
                    if domain != list(domainList)[-1] or target != targetList[-1]:
                        printT(rtDel([17,20,10,10,10,10,10,37,10,22]),"middle")
                    else:
                        printT(rtDel([17,20,10,10,10,10,10,37,10,22]),"bottom")
                else:
                    result = [target, domain, rankDict["baiduRank"], rankDict["yidongRank"], rankDict["360Rank"], rankDict["sougouRank"],rankDict["googleRank"] ]
                    tableDataList=[
                        [result[0], 17],
                        [result[1], 20],
                        [result[2], 10],
                        [result[3], 10],
                        [result[4], 10],
                        [result[5], 10],
                        [result[6], 10]
                    ]
                    printT(rtDel(tableDataList))
                    csvWriter.writerow(result)
                    if domain != list(domainList)[-1] or target != targetList[-1]:
                        printT(rtDel([17,20,10,10,10,10,10]),"middle")
                    else:
                        printT(rtDel([17,20,10,10,10,10,10]),"bottom")
                break

def getTitle(mode=""):
    if args.icp:
        printT(rtDel([17,20,10,10,10,10,10,37,10,22]),"top")
        tableDataList=[
            ["ip/domain",17],
            ["反查域名",20],
            ["百度权重",10],
            ["移动权重",10],
            ["360权重",10],
            ["搜狗权重",10],
            ["谷歌权重",10],
            ["单位名称",37],
            ["单位性质",10],
            ["备案编号",22]
        ]
        printT(rtDel(tableDataList),fontStyle="bold")
        printT(rtDel([17,20,10,10,10,10,10,37,10,22]),"middle")
        csvWriter.writerow(["ip/domain", "反查域名", "百度权重", "移动权重", "360权重", "搜狗权重", "谷歌权重", "单位名称", "单位性质", "备案编号"]) if mode!="OnlyPrint" else 0
    else:
        printT(rtDel([17,20,10,10,10,10,10]),"top")
        tableDataList=[
            ["ip/domain",17],
            ["反查域名",20],
            ["百度权重",10],
            ["移动权重",10],
            ["360权重",10],
            ["搜狗权重",10],
            ["谷歌权重",10]
        ]
        printT(rtDel(tableDataList),fontStyle="bold")
        printT(rtDel([17,20,10,10,10,10,10]),"middle")
        csvWriter.writerow(["ip/domain", "反查域名", "百度权重", "移动权重", "360权重", "搜狗权重", "谷歌权重"]) if mode!="OnlyPrint" else 0

if __name__ == "__main__":
    fistDate = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    fistTime = time.time()

    args = parseArgs()

    targetList = loadTarget(args.file, args.target)

    outFilePath = f"./Result/{args.output}.csv"
    os.mkdir(r"./Result") if not os.path.isdir(r"./Result") else 0
    existFile = True if os.path.exists(outFilePath) else False
    file = open(outFilePath, "a+", encoding="GBK", newline="")
    csvWriter = csv.writer(file)

    getTitle()  if not existFile else getTitle("OnlyPrint")

    for target in targetList:
        getIpInfo(target)

    finallyDate = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    finallyTime = time.time()
    timing = (finallyTime-fistTime)
    print(printTime()+"查询完毕，用时：%f秒"%(timing))
    print(printTime()+f"结果已保存至：{outFilePath}")