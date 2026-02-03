## CI/CD Pipeline Status

[![Lint](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/-/jobs/artifacts/main/raw/lint.svg?job=lint)](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/-/pipelines)
[![Format](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/-/jobs/artifacts/main/raw/format.svg?job=format)](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/-/pipelines)

### Linux (dev-режим)
1. `git clone <URL_РЕПО>`
2. `cd lyceum`
3. `python3 -m venv venv`
4. `source venv/bin/activate`
5. `cp template.env .env` 
6. `pip install -r requirements/prod.txt`
7. `python manage.py migrate`
8. `python manage.py runserver`