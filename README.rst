=================
DITA Link Checker
=================
About
-----
The sctipt is useful for checking if linked files exest of not before generating output materials with DITA Open Toolkit.

Usage
-----
Use it in package file before running DITA-OT. Example for BAT-file:
::

	REM run script to check links. if error then exit and open errorpage with indicators
	python %PATH_TO_SCRIPT%dita-xrefs.py
	IF %ERRORLEVEL% == 1 (
		pause
		%PATH_TO_SCRIPT%xrefs.html
		exit
	)
