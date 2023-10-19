# APP BMR

Back-End for the BMR fast food restaurant

## Requirements

Python 3.11 +
Django 4.2
Django Rest Framework 3.14
SQLite (PostgreSQL in a future)
Djoser 2.2
PyJWT 2.8
Django Rest Framework Simple Jwt 5.3

## Installation

By Default the database is SQLITE

1. Clone this repository:
    git clone: https://github.com/BonifacioJZ/AppBMR.git

2. Generate Virtual ENV
python -m venv venv
source venv/bin/activate   On Unix/Linux systems
Or on Windows systems
venv\Scripts\activate
pip install -r requirements.txt

Configure the database in settings.py.

# Generate the .env with the database information (At the moment it is only for SQLite)
Apply database migrations:

python manage.py makemigrations
python manage.py migrate
# Usage
Explain how to use your application, including how to run it locally and interact with the API endpoints.

Example:

To run the application locally, use the following command:
python manage.py runserver






