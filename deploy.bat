@echo off
"C:\Program Files (x86)\WinSCP\WinSCP.com" /command ^
    "open sftp://enzon:gumball@192.168.1.172/" ^
    "put C:\raspb\Repo\Robot\*.py /home/enzon/" ^
    "put C:\raspb\Repo\Robot\sensors\*.py /home/enzon/sensors/" ^
    "put C:\raspb\Repo\Robot\motors\*.py /home/enzon/motors/" ^
    "put C:\raspb\Repo\Interface\templates\index.html /home/enzon/templates/" ^
    "put C:\raspb\Repo\Interface\static\style.css /home/enzon/static/" ^
    "exit"
echo Transfert terminé !
pause