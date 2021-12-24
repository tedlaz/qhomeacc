pyinstaller -F -w --icon=homeacc.ico qhomeacc.py
copy .\dist\qhomeacc.exe .
rd /S /Q dist
rd /S /Q build
del .\qhomeacc.spec
