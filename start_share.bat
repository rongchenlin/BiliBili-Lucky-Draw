@echo off
echo "start ..."
C:\Users\Administrator\Desktop\Bilibili
cd venv
cd Scripts
call activate.bat
cd ../..
python do_share.py
pause