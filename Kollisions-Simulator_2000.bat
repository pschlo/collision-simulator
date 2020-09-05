<# : chooser.bat
@echo off
setlocal
echo Es wird versucht, Kollisions-Simulator 2000 zu starten...
echo.
_main.py
if errorlevel 1 goto :2
goto :finish

:2
python _main.py >nul 2>&1
if errorlevel 1 goto :3
goto :finish

:fail
echo.
echo Kollisions-Simulator 2000 konnte nicht gestartet werden :(
echo.
echo.
echo Zum Beenden Taste druecken...
pause>nul
goto :EOF

:finish
echo.
echo Kollisions-Simulator wurde beendet.
echo.
echo.
echo Zum Beenden Taste druecken...
pause>nul
goto :EOF


:3
echo.
echo Bitte waehle die Python-Installation manuell aus
for /f "delims=" %%I in ('powershell -noprofile "iex (${%~f0} | out-string)"') do (
    set python_path=%%~I
)

"%python_path%" _main.py >nul 2>&1
if errorlevel 1 goto :fail
goto :finish


: end Batch portion / begin PowerShell hybrid chimera #>

Add-Type -AssemblyName System.Windows.Forms
$f = new-object Windows.Forms.OpenFileDialog
$f.InitialDirectory = pwd
$f.Filter = "EXE-Dateien (*.exe)|*.exe"
$f.ShowHelp = $false
$f.Multiselect = $true
[void]$f.ShowDialog()
if ($f.Multiselect) { $f.FileNames } else { $f.FileName }