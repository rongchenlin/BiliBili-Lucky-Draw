@echo off
echo "start ..."
cd C:\Users\Administrator\Desktop\Bilibili
cd venv
cd Scripts
call activate.bat
cd ../..
python get_user.py
pause