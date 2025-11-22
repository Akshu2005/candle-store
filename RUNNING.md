# How to run locally

1. Create & activate venv:
   python -m venv venv
   venv\Scripts\activate    (Windows) or source venv/bin/activate (mac/linux)

2. Install:
   pip install -r requirements.txt

3. Make migrations & migrate:
   python manage.py makemigrations
   python manage.py migrate

4. Create superuser:
   python manage.py createsuperuser

5. Load fixtures (adds categories and products):
   python manage.py loaddata shop/fixtures/fixtures.json

6. Run server:
   python manage.py runserver
