# API YaMDb
YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.

## Стек технологий
Python 3.9.4, Django 3.1+, Django REST Framework, SQLite3, Simple JWT, Django Filter.

### Установка
Создайте виртуальное окружение:

`python -m venv venv`

Активация виртуального окружения:

`source venv/bin/activate`

Используйте pip, чтобы установить зависимости:

`pip install -r requirements.txt`

После создайте в корневой директории файл с названием ".env" и поместите в него:

`SECRET_KEY=любой_секретный_ключ_на_ваш_выбор`

`DEBUG=False`

`ALLOWED_HOSTS=*`

Примените миграции:

`python manage.py migrate`

Запуск сервера:

`python manage.py runserver`
