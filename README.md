# ipInfoSearch
ip域名反查、权重查询以及ICP备案查询。便于提交SRC时资产过滤。

## 配置需要python三方包
pip install -r requirements.txt

## 基本用法：
python ipInfoSearch.py -h
![image](/img/help.png)

python ipInfoSearch.py -f fileName.txt -icp -o outFileName
![image](/img/ipInfoSearch1.png)
![image](/img/ipInfoSearch2.png)

## 多线程用法：
python runThread.py -c "python ipInfoSearch.py -t {{data}} -icp -o outFileName" -f fileName.txt
注释：只需修改outFileName 以及 fileName
原理：遍历fileName填充{{data}}执行命令
![image](/img/runThread1.png)
![image](/img/runThread2.png)
