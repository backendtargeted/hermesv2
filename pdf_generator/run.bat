@echo off
echo Starting PDF Generator...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting the application...
echo Open your browser and go to: http://localhost:5001
echo.
python app.py
pause
