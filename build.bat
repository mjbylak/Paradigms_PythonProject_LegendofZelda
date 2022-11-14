::@echo off
python game.py
if %errorlevel% neq 0 (
	echo There was an error; exiting now.
	pause
	
) else (ds
	echo Compiled correctly!  Running Game...
	java Game	
)

