@echo off
REM One-shot setup for Windows.

echo ==^> Creating virtual environment
python -m venv .venv
call .venv\Scripts\activate.bat

echo ==^> Installing Django
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ==^> Building the database
python manage.py makemigrations core
python manage.py migrate

echo ==^> Loading the menu, awards and sample reviews
python manage.py seed_data

echo.
echo Done. Two things left:
echo   1. python manage.py createsuperuser   (to log in to /admin/)
echo   2. python manage.py runserver         (then open http://127.0.0.1:8000)
echo.
pause
