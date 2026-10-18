@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  python -m venv .venv
  if errorlevel 1 goto setup_failed
  .venv\Scripts\python.exe -m pip install --upgrade pip
  .venv\Scripts\python.exe -m pip install -e .
  if errorlevel 1 goto setup_failed
)
.venv\Scripts\python.exe -m streamlit run src/privacy_blur/app.py
pause
goto :eof

:setup_failed
echo Setup failed. Check that Python 3.11 or newer is installed and available as "python".
pause
