import time

import requests

proxy_ip_url = "http://dev.qydailiip.com/api/?apikey=b14d7f87f24eba0f8042cc1960ec32e0080cbfa6&num=50&type=json&line=win&proxy_type=putong&sort=1&model=all&protocol=http&address=&kill_address=&port=&kill_port=&today=false&abroad=&isp=&anonymity=2"

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}

URL_LIST = [
    "http://jobs.zhaopin.com/CCL1241526860J00505295507.htm",
    "http://jobs.zhaopin.com/CCL1241526860J00505296007.htm",
    "http://jobs.zhaopin.com/CCL1241526860J00505295907.htm"
]

clicked = 0

while clicked < 1000:
    try:
        ips = eval(requests.get(proxy_ip_url).text)
    except Exception as E:
        print("获取代理IP出错, 休眠5秒钟后重试")
        time.sleep(5)
        continue

    for index in range(len(ips)):
        ip = ips[index]

        try:
            test = requests.get("http://icanhazip.com/", headers=HEADERS, proxies={"http": ip}, timeout=20)
        except requests.exceptions.ConnectionError as E:
            print("http:" + ip + " 验证未通过 ConnectionError 异常")
            print(E)
            continue
        except Exception as E:
            print("http:" + ip + " 验证未通过 ConnectionError 异常")
            print(E)
            continue

        if test.text.rstrip("\n") == ip.split(":")[0]:
            print("http:" + ip + " 验证已通过")
            num = 0
            for each_url in URL_LIST:
                num = 0
                try:
                    response = requests.get(each_url, headers=HEADERS, proxies={"http": ip}, timeout=20)
                    if response.status_code == 200:
                        print("http:" + ip + " 请求 " + each_url + " 页面 成功, 当前点击量: " + str(clicked))
                except requests.exceptions.ConnectionError:
                    print("http:" + ip + " 请求 " + each_url + " 页面 发现代理")
                    break
                except Exception as E:
                    print("http:" + ip + " 请求 " + each_url + " 页面 异常")
                    print(E)
                else:
                    num += 1
            if num > 0:
                clicked += 1
            continue

        else:
            print("http:" + ip + " 验证未通过 代理IP不一致异常: " + test.text.rstrip("\n"))
            continue
