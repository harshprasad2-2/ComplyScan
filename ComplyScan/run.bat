@echo off
REM ComplyScan Launcher for Windows

echo.
echo ======================================
echo  ComplyScan - Legal Metrology Scanner
echo ======================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run Streamlit app
python -m streamlit run app.py

REM Pause on exit
pause
