@echo off
echo Updating TapFo Gallery Folders...
python update_manifests.py
echo.
echo Launching TapFo in your browser...
start index.html
exit
