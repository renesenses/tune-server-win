@echo off
title Tune Server
cd /d "%~dp0"

if not exist .env (
    echo Creating default .env file...
    echo MUSIC_DIRS=C:\Users\%USERNAME%\Music> .env
    echo API_PORT=8888>> .env
    echo .env created - edit it to set your music directory.
    echo.
)

echo Starting Tune Server...
echo Web UI: http://localhost:8888
echo.
tune-server.exe
pause
