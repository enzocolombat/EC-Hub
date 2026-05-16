@echo off
"C:\Program Files (x86)\WinSCP\WinSCP.com" /command ^
    "open sftp://enzon:gumball@192.168.1.172/" ^
    "put C:\raspb\Repo\Robot\*.py /home/enzon/" ^
    "exit"
echo Transfert terminé !
pause