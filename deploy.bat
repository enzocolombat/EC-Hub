@echo off
for /f "tokens=1,2 delims==" %%a in (.env) do set %%a=%%b
"C:\Program Files (x86)\WinSCP\WinSCP.com" /command ^
    "open sftp://%PI_USER%:%PI_PASS%@%PI_IP%/" ^
    "put C:\raspb\Repo\Robot\server.py /home/enzon/Robot/" ^
    "put C:\raspb\Repo\Robot\sensors\*.py /home/enzon/Robot/sensors/" ^
    "put C:\raspb\Repo\Robot\motors\*.py /home/enzon/Robot/motors/" ^
    "put C:\raspb\Repo\Interface\templates\*.html /home/enzon/interface/templates/" ^
    "put C:\raspb\Repo\Interface\static\*.css /home/enzon/interface/static/" ^
    "put C:\raspb\Repo\Interface\static\*.js /home/enzon/interface/static/" ^
    "put C:\raspb\Repo\*.txt /home/enzon/" ^
    "exit"
echo Transfer complete!
pause