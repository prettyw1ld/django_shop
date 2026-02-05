[![pipeline status](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/-/commits/main)

# Lyceum (проект на Django)
Учебный проект с ипользованием фреймворка Django. 

## Технологии
- [Django](https://docs.djangoproject.com/en/5.2/)
- [Python](https://docs.python.org/3/whatsnew/3.12.html)
- [GitLab](https://docs.gitlab.com/)

## Использование
Чтобы установить и запустить проект на Linux, нужно выполнить следующие действия:

Клонировать репозиторий с помощью команды:
```sh
git clone https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585.git
```

Далее перейти в папку с проектом:
```sh
cd lyceum
```

Создание виртуального окружения:
```sh
python3 -m venv venv
```
Активация: 
```sh
source venv/bin/activate
```
Теперь нужно клонировать файл-шаблон с переменными окружения:
```sh
cp template.env .env
```
<sub> (p.s. конечно же надо будет заполнить потом настоящие данные, а не оставлять как есть :D) </sub>


Установка основных зависимостей:
```sh
pip install -r requirements/prod.txt
```

Далее можно выполнить команду миграции, чтобы при запуске на нас не ругался терминал:
```sh
python manage.py migrate
```

Запуск приложения:
```sh
python manage.py runserver
```

## CI/CD
В файле [.gitlab-ci.yml](Lection/.gitlab-ci.yml) ностроены первоначальные проверки. Пайплан будет запускаться сразу же после коммита в репозиторий.

## Команда проекта
- **Дамир** (я) - разработчик и лид проекта
- **Деник** (кот) - моральная поддержка и тестирование методом хождения по клавиатуре

## Зачем вы разработали этот проект?
Чтобы был.