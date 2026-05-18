@echo off
for /f "tokens=1,2 delims==" %%a in (.env) do set %%a=%%b
"C:\Program Files (x86)\WinSCP\WinSCP.com" /command ^
    "open sftp://%PI_USER%:%PI_PASS%@%PI_IP%/" ^
    "put C:\raspb\Repo\Robot\server.py /home/enzon/" ^
    "put C:\raspb\Repo\Robot\sensors\*.py /home/enzon/sensors/" ^
    "put C:\raspb\Repo\Interface\templates\*.html /home/enzon/templates/" ^
    "put C:\raspb\Repo\Interface\static\*.css /home/enzon/static/" ^
    "exit"
echo Transfert terminé !
pause