#!/bin/sh

# Применяем миграции
python manage.py migrate

# Запускаем сервер
gunicorn --workers=4 -b 0.0.0.0:8000 my_project.wsgi:application