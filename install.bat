@echo off
title Tune Server - Installation
echo.
echo  ╔══════════════════════════════════════╗
echo  ║     Tune Server - Installation       ║
echo  ╚══════════════════════════════════════╝
echo.

:: Create desktop shortcut
echo Creating desktop shortcut...
set SCRIPT="%TEMP%\create-shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Tune Server.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0start-tune-server.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.IconLocation = "%~dp0tune-server.ico" >> %SCRIPT%
echo oLink.Description = "Tune Server - Multi-room audio" >> %SCRIPT%
echo oLink.WindowStyle = 7 >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

echo.
echo  [OK] Desktop shortcut created: "Tune Server"
echo.
echo  To start Tune Server:
echo    - Double-click "Tune Server" on your desktop
echo    - Or run start-tune-server.bat from this folder
echo.
echo  Web UI: http://localhost:8888
echo.
pause
