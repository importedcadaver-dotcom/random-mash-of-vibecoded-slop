@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Python environment missing. Please run setup.ps1 first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" main.py
if errorlevel 1 (
  echo.
  echo The game stopped with an error. Please send this window's output for troubleshooting.
  pause
)
