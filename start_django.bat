@echo off
cd /d "C:\Users\Sathvika\Documents\VSCODE\delightapi"
call .\aptpath\Scripts\activate.bat
cd AptPath-DelightAPI
echo Starting Django server...
python manage.py runserver
pause
