@echo off
python build_defines_setter.py develop
pyarmor pack -x"--exclude venv --exclude localization" -e"--onefile --icon=icon.ico" TinderBot.py
pause