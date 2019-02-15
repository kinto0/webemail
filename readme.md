# Django webapp for sending email updates about weather

- To start, clone repo and type `python manage.py runserver` in the terminal at the root directory. 
- Run `python manage.py import_cities` to import the top 100 cities by population into the database. 
- Navigate to localhost:8000 and add some email addresses and locations to your mailing list. 
- Run `python manage.py send_mail` to send an email updating your mailing list with the current weather. 
