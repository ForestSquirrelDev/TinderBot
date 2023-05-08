@echo off
python build_defines_setter.py production
pyarmor pack -x"--exclude venv --exclude localization" -e"--onefile --windowed --icon=icon.ico" TinderBot.py
signtool sign /f sign\forestsquirreldev.pfx /p 123 /t http://timestamp.digicert.com /v dist/TinderBot.exe
pause