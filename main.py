import requests
from config import *
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
import re
import traceback

url = "https://legulegu.com/stockdata/marketcap-gdp"

headers = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7
Cache-Control: max-age=0
Connection: keep-alive
Cookie: 97C7DB=af5e8ed2-df5d-4e8b-b6fc-4cba63896ba4; JSESSIONID=3A2FB3B8B7C970F966F72658648BEEDD; Hm_lvt_4064402dbf370b44e70272f9f2632a67=1707900757; _gid=GA1.2.1397034982.1707900758; __gads=ID=50f9adf4ead0b3ef:T=1707900758:RT=1707900758:S=ALNI_Ma8aSgEY5HSSJeBqIKvCrgJeYfRyg; __gpi=UID=00000d06b85f6053:T=1707900758:RT=1707900758:S=ALNI_MY63AqjOKJWouyNlF-u6YOYQgoDAg; __eoi=ID=74b8d5882c60217e:T=1707900758:RT=1707900758:S=AA-AfjamMHQ7Mg3Zwtb_IFLPKAI6; FCNEC=%5B%5B%22AKsRol8YgnC_NzbZLgrhq_reDkZA9jJxFtwYD1v7z4PyqkiOjgwV6AAgPfMu1I8KefAroHNd-pNjUFgs8FdMXNME-4VdBCoMqTnYL6YOKruXkmsWouvnVC-Lz0YVeSijKbmPRij-4uxrx4IZlz6NJoTCTs27eY3hHw%3D%3D%22%5D%5D; Hm_lpvt_4064402dbf370b44e70272f9f2632a67=1707900835; _gat_gtag_UA_117119777_1=1; _ga_5YD2TJWE1T=GS1.1.1707900757.1.1.1707900835.0.0.0; _ga=GA1.1.1401586768.1707900758
Host: legulegu.com
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36
sec-ch-ua: "Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
'''


#headers转换
def trans(s):
    d = dict()
    s = s.split("\n")
    for i in s:
        if (i == ''):
            continue
        if (i[0] == ":"):
            i = i[1:]
        d[i.split(': ')[0]] = i.split(': ')[1]
    return d


def sendMail(user,password,message,Subject,sender_show,recipient_show,to_addrs,cc_show=''):
    '''
    :param message: str 邮件内容
    :param Subject: str 邮件主题描述
    :param sender_show: str 发件人显示，不起实际作用如："xxx"
    :param recipient_show: str 收件人显示，不起实际作用 多个收件人用','隔开如："xxx,xxxx"
    :param to_addrs: str 实际收件人
    :param cc_show: str 抄送人显示，不起实际作用，多个抄送人用','隔开如："xxx,xxxx"
    '''
    # 邮件内容
    msg = MIMEText(message, 'html', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = Subject
    # 发件人显示，不起实际作用
    msg["From"] = sender_show
    # 收件人显示，不起实际作用
    msg["to"] = recipient_show
    # 抄送人显示，不起实际作用
    msg["Cc"] = cc_show
    try:
        with SMTP_SSL(host="smtp.qq.com",port=465) as smtp:
            # 登录发送邮件服务器
            smtp.login(user = user, password = password)
            # 实际发送、接收邮件配置
            smtp.sendmail(from_addr = user, to_addrs=to_addrs.split(','), msg=msg.as_string())
    except:
        print("发送邮件失败")
        traceback.print_exc()
n=3
while(n):
    try:
        r = requests.get(url, headers=trans(headers))
        searchObj = re.search("总市值比GDP值为：(.*?)%", r.text)
        n = float(searchObj.group(1))
        break
    except:
        print("获取失败")
        traceback.print_exc()
        sendMail(
        user, password,
        f"乐股数据获取失败 第{4-n}次尝试 {traceback.format_exc()}",
        f"乐股数据获取失败", to_addrs,to_addrs,to_addrs)
        n-=1

if (n >= upper):
    # 达到上限
    sendMail(
        user, password,
        f"达到上限,总市值比GDP值为：{n}% https://legulegu.com/stockdata/marketcap-gdp",
        f"达到上限,总市值比GDP值为：{n}%", to_addrs,to_addrs,to_addrs)
    print(f"达到上限,总市值比GDP值为：{n}")

if (n <= down):
    # 达到下限
    sendMail(
        user, password,
        f"达到下限,总市值比GDP值为：{n}% https://legulegu.com/stockdata/marketcap-gdp",
        f"达到下限,总市值比GDP值为：{n}%", to_addrs,to_addrs,to_addrs)
    print(f"达到下限,总市值比GDP值为：{n}")


