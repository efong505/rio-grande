release: python manage.py makemigrations & python manage.py migrate --no-input & wait -n
web: gunicorn julias2.wsgi
