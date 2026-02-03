# Lyceum Django Project [![Pipeline status](https://gitlab.crja72.ru/api/v4/projects/3798/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/-/pipelines)

### Linux (dev-режим)
1. `git clone <URL_РЕПО>`
2. `cd lyceum`
3. `python3 -m venv venv`
4. `source venv/bin/activate`
5. `cp template.env .env` 
6. `pip install -r requirements/prod.txt`
7. `python manage.py migrate`
8. `python manage.py runserver`