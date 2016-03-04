Make sure you have MySQLServer running in your local environment before deploying the application with WSGI:
"mysql.server start"
"python manage.py runserver"

You can access the website locally via http://127.0.0.1:8000/

Make changes to DB:
1. change models (in models.py)
2. Run "python manage.py makemigrations" to create migrations for those changes
3. Run "python manage.py migrate" to apply those changes to the database