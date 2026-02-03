Установка и запуск (Linux, dev-режим)

1) git clone <URL_РЕПО>
2) cd lyceum
3) python3 -m venv venv
4) source venv/bin/activate
5) cp template.env .env
6) pip install -r requirements/prod.txt
7) python manage.py migrate
8) python3 manage.py runserver