@echo off
"C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\windbg.exe" -a pykd.pyd -c "!py -g winext\TWindbg\TWindbg.py"
