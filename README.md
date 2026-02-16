# Lyceum (проект на Django)
Учебный проект с ипользованием фреймворка Django. 


[![pipeline status](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/badges/main/pipeline.svg?key_text=lint/test)](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/-/commits/main)


## Необходимое ПО
- [Django](https://www.djangoproject.com/download/)
- [Python](https://www.python.org/downloads/release/python-3120/)
- [Git](https://git-scm.com/install/windows)

## Использование
Чтобы установить и запустить проект на Linux, нужно выполнить следующие действия:

Клонировать репозиторий с помощью команды:
```sh
git clone https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585.git lyceum
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

Далее перейти в папку с manage.py:
```sh
cd lyceum
```

Далее можно выполнить команду миграции, чтобы при запуске на нас не ругался терминал:
```sh
python manage.py migrate
```

Запуск приложения:
```sh
python manage.py runserver localhost:8000
```

## CI/CD
В файле [.gitlab-ci.yml](https://gitlab.crja72.ru/django/2026/spring/course/students/377070-damirkhodzhiev-course-1585/-/blob/main/.gitlab-ci.yml) ностроены первоначальные проверки. Пайплан будет запускаться сразу же после коммита в репозиторий.

## Команда проекта
- **Дамир** (я) - разработчик и лид проекта
- **Деник** (кот) - моральная поддержка и тестирование методом хождения по клавиатуре

## Зачем вы разработали этот проект?
Чтобы был.