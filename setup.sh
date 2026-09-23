#!/usr/bin/env bash
# One-shot setup for macOS / Linux.
set -e

echo "==> Creating virtual environment"
python3 -m venv .venv
source .venv/bin/activate

echo "==> Installing Django"
pip install --upgrade pip >/dev/null
pip install -r requirements.txt

echo "==> Building the database"
python manage.py makemigrations core
python manage.py migrate

echo "==> Loading the menu, awards and sample reviews"
python manage.py seed_data

echo ""
echo "Done. Two things left:"
echo "  1. python manage.py createsuperuser   (to log in to /admin/)"
echo "  2. python manage.py runserver         (then open http://127.0.0.1:8000)"
echo ""
echo "Remember to run 'source .venv/bin/activate' in new terminal windows."
