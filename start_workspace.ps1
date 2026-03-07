 = 'd:\work_home\neverAloneInCheapRental'
 = 'd:\work_home\neverAloneInCheapRental\art\concepts\characters'
Write-Host 'Starting workspace...'
Start-Process explorer 
Start-Process explorer 
Write-Host 'Press any key to launch Stable Diffusion WebUI (Forge)...'
System.Management.Automation.Internal.Host.InternalHost.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') | Out-Null
Set-Location -Path 'd:\work_home\neverAloneInCheapRental\tools\stable-diffusion-webui-forge'
if (Test-Path 'webui-user.bat') { Start-Process 'webui-user.bat' } else { Write-Host 'Forge webui-user.bat not found.' }
