import subprocess
import re
from urllib2 import urlopen
from json import load
import socket
import struct
import random




iplist = ['192.168.0.1/24',
 '192.168.1.1/24',
 '192.168.2.1/24',
 '192.168.3.1/24',
 '192.168.4.1/24',
 '192.168.5.1/24',
 '192.168.6.1/24',
 '192.168.7.1/24',
 '192.168.8.1/24',
 '192.168.9.1/24',
 '192.168.10.1/24',
 '192.168.18.1/24',
 '192.168.31.1/24',
 '192.168.199.1/24',
 '192.168.254.1/24',
 '192.168.67.1/24',
 '10.0.0.1/24',
 '10.0.1.1/24',
 '10.0.2.1/24',
 '10.1.1.1/24',
 '10.90.90.1/24',
 '10.1.10.1/24',
 '10.10.1.1/24']

def find_ip():
    global iplist2
    ipconfig_process = subprocess.Popen('ipconfig /all', stdout=subprocess.PIPE)
    output = ipconfig_process.stdout.read()
    result = re.findall('\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b', output)
    for ipaddr in result:
        if ipaddr != '127.0.0.1' and ipaddr != '255.255.255.0' and ipaddr != '0.0.0.0':
            ipaddr = ipaddr.split('.')[0] + '.' + ipaddr.split('.')[1] + '.' + ipaddr.split('.')[2] + '.1/24'
            iplist.append(ipaddr)

    netstat_process = subprocess.Popen('netstat -na', stdout=subprocess.PIPE)
    output2 = netstat_process.stdout.read()
    result2 = re.findall('\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b', output2)
    for ip in result2:
        if ip != '127.0.0.1' and ip != '0.0.0.0' and ip != '255.255.0.0' and ip != '1.1.1.1':
            ip = ip.split('.')[0] + '.' + ip.split('.')[1] + '.' + ip.split('.')[2] + '.1/24'
            iplist.append(ip)

    try:
        ipp1 = urlopen('http://ip.42.pl/raw', timeout=3).read()
        ipp1 = ipp1.split('.')[0] + '.' + ipp1.split('.')[1] + '.' + ipp1.split('.')[2] + '.1/24'
        ipp2 = load(urlopen('http://jsonip.com', timeout=3))['ip']
        ipp2 = ipp2.split('.')[0] + '.' + ipp2.split('.')[1] + '.' + ipp2.split('.')[2] + '.1/24'
        iplist.append(ipp1)
        iplist.append(ipp2)
    except:
        pass

    iplist2 = list(set(iplist))
    iplist2.sort(key=iplist.index)
    return iplist2

nip = []
def xip(numb=500):
    del nip[:]
    for n in xrange(numb):
        ipp = socket.inet_ntoa(struct.pack('>I', random.randint(1, 4294967295L)))
        ipp = ipp.split('.')[0] + '.' + ipp.split('.')[1] + '.' + ipp.split('.')[2] + '.1/24'
        nip.append(ipp)

    return nip

# for s in xip(500):
#     if s.split('.')[0].strip() == '127':
#         continue
#     if s.split('.')[0].strip() == '10':
#         continue
#     if s.split('.')[0].strip() == '0':
#         continue
#     if s.split('.')[0].strip() == '100':
#         continue
#     if s.split('.')[0].strip() == '172':
#         continue
#     if int(s.split('.')[0].strip()) in xrange(224, 256):
#         continue
#     # print(s)
#     ip, cidr = s.split('/')
#     cidr = int(cidr)
#     host_bits = 32 - cidr
#     i = struct.unpack('>I', socket.inet_aton(ip))[0]
#     start = i >> host_bits << host_bits
#     end = i | (1 << host_bits) - 1
#     for i in range(start + 1, end):
#         # semaphore1.acquire()
#         ip = socket.inet_ntoa(struct.pack('>I', i))
#         print(ip)
#         # t1 = threading.Thread(target=scansmb2, args=(ip, 445))
#         # t1.start()

def scan2(ip, p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(float(2))
    try:
        s.connect((ip, p))
        return 1
    except Exception as e:
        return 0


if __name__ == "__main__":
    value = scan2("127.0.0.1", 445)
    print(value)