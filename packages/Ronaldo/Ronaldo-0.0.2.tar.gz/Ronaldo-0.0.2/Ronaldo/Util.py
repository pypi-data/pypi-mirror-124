
import json
from lxml import etree
import requests
from colorama import Fore
import re
import socket

def getmyip():
    r = requests.get("https://ip.cn/api/index?ip=&type=0")
    ip = json.loads(r.text)
    print(Fore.RED + "Your Internel Ip:\t" + ip["ip"]+"\t"+ip["address"])

def isip(ip):
    result = re.match('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$',ip)
    return result
def isdomain(domain):
    result = re.match('[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+\.?',domain)
    return result
#IPπÈ Ùµÿ
def getip(ip):
    r = requests.get("https://ip.cn/ip/{}.html".format(ip))
    tree = etree.HTML(r.text)
    addr = tree.xpath('//*[@id="tab0_address"]/text()')
    return addr[0]
#IP∑¥≤È
def getdomain(ip):
    domain = []
    r= requests.get('http://ip.yqie.com/iptodomain.aspx?ip={}'.format(ip))
    tree = etree.HTML(r.text)
    count = int(tree.xpath('//*[@id="yhide"]/text()')[0])
    for i in range(3,3+count):
        result = tree.xpath('/html/body/div[1]/div[8]/table/tr[{}]/td[2]/text()'.format(i))[0]
        if isdomain(result):
            domain.append(result)
    return domain


def domaingetip(domain):
    return socket.gethostbyname(domain)