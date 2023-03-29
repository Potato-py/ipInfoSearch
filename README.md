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

## 报错处理：

- 若报错：RuntimeError: maximum recursion depth exceeded

- 是因为性能低导致的递归问题，请在ipInfoSearch.py头部添加

```
import sys
sys.setrecursionlimit(10000)
```

## 多线程用法：
python runThread.py -c "python ipInfoSearch.py -t {{data}} -icp -o outFileName -hidden" -f fileName.txt

注释：**只需修改outFileName 以及 fileName**

注释：**-hidden 为ipInfoSearch.py参数，多线程不打印干扰信息**

原理：遍历fileName填充{{data}}执行命令

![image](/img/runThread1.png)

![image](/img/runThread2.png)
