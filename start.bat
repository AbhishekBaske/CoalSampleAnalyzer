@echo off
echo ========================================
echo   Coal Spontaneous Combustion Analyzer
echo ========================================
echo.
echo Starting the application...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo Installing/updating requirements...
pip install -r requirements.txt

REM Start the application
echo.
echo Starting Flask application...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause