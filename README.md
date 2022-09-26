# ipInfoSearch
ip域名反查、权重查询以及ICP备案查询。便于提交SRC时资产过滤。

基本用法：
python ipInfoSearch.py -f fileName.txt -icp -o outFileName

多线程用法：
python runThread.py -c "python ipInfoSearch.py -t {{data}} -icp -o outFileName" -f fileName.txt
