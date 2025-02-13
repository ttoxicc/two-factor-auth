@echo off

start "Web Server" python app.py
start "Telegram Bot" python bot_registration.py

echo Нажмите любую клавишу для остановки...
pause > nul

taskkill /FI "WINDOWTITLE eq Web Server" /F
taskkill /FI "WINDOWTITLE eq Telegram Bot" /F