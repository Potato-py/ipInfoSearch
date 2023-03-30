from concurrent.futures import ThreadPoolExecutor
import subprocess
import time
import argparse
import os
import sys

def parseArgs():
    fistDate = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest="num", required=False, type=int, default=60, help=f"最大线程数（默认60）")
    parser.add_argument("-c", dest="command", required=True, type=str, help="执行的命令（需要遍历部分请用{{data}}代替，并传入-f）")
    parser.add_argument("-f", dest="file", required=False, type=str, help=f"需要遍历数据的文件")
    parser.add_argument("-o", dest="output", required=False, type=str, default=f"{fistDate}", help=f"输出文件 (默认输出 ./Result/{fistDate}.txt)")
    argsObj = parser.parse_args()
    if not argsObj.command or ( "{{data}}" in argsObj.command and not argsObj.file ):
        print('\033[31m\n[Info] 多线程内部若存在输出文件，请改用时间戳命名或a+追加方式，防止覆盖输出\n[Info] 若需加载文件，启动命令需转换为单个目标 \n[x] 用法:python runThread.py [-n 线程数] [-c 执行的命令] [-f 需要遍历数据的文件] [-o 输出文件名]\n\n[-] 举例:python runThread.py -n 60 -c "python3 ipInfoSearch.py -t {{data}} -ipc -o csvOut -hidden" -f ./fileData.txt -o ipInfoText\033[0m')
        sys.exit()
    if argsObj.file:
        if not os.path.isfile(argsObj.file):
            print(f"\033[31m[Error] 加载文件[{argsObj.file}]失败\033[0m")
            sys.exit()
    print(f"[Info] -n    ：  {argsObj.num}")
    print(f"[Info] -c    ：  {argsObj.command}")
    print(f"[Info] -f    ：  {argsObj.file}")
    print(f"[Info] -o    ：  ./Result/{argsObj.output}.txt")
    print(f"[Info] 多线程内部若存在输出文件，请改用时间戳命名或a+追加方式，防止覆盖输出")
    print(f"[Info] 若需加载文件，启动命令需转换为单个目标")

    return argsObj

def runThread():
    start = time.time()

    targetList = []
    if args.file:
        file = open(args.file, encoding="utf8")
        for line in file.readlines():
            targetData = line.strip()
            if targetData and targetData not in targetList:
                targetList.append(targetData)
        file.close()

    #   创建线程
    with ThreadPoolExecutor(max_workers=args.num) as executor:
        if len(targetList)>1:
            [ executor.submit(func, args.command.replace("{{data}}",f"\"{i}\"")) for i in targetList ]
        else:
            [ executor.submit(func, args.command) for i in range(args.num) ]

    end = time.time()
    print(f'\033[32mProgram takes time: {end - start}\033[0m')

def func(command):
    #多线程 转 多进程
    cmd = subprocess.run(command, shell=True)



if __name__ == "__main__":
    args = parseArgs()
    runThread()
