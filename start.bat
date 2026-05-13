@echo off
echo Starting VartaIQ AI Meeting Analyzer...

if not exist venv (
    echo Creating virtual environment with Python 3.10...
    py -3.10 -m venv venv
    echo Installing dependencies...
    venv\Scripts\pip install -r requirements.txt
)

call venv\Scripts\activate.bat
python run.py
