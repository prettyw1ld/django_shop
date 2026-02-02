Установка и запуск (Linux, dev-режим)

1) git clone <URL_РЕПО>
2) cp template.env .env
3) cd lyceum
4) python3 -m venv venv
5) source venv/bin/activate
6) pip install -r requirements.txt
7) python manage.py migrate
8) python3 manage.py runserver
