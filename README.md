# Habit Tracker API

Бэкенд для трекера полезных привычек на основе книги "Атомные привычки" Джеймса Клира.

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте окружение: `venv\Scripts\activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Создайте файл `.env` и настройте переменные окружения
6. Примените миграции: `python manage.py migrate`
7. Создайте суперпользователя: `python manage.py createsuperuser`
8. Запустите сервер: `python manage.py runserver`

## API Endpoints

- `GET/POST /api/my_habits/` - Мои привычки
- `GET /api/public_habits/` - Публичные привычки
- `POST /api/auth/token/` - Получение JWT токена
- `POST /api/auth/token/refresh/` - Обновление токена

## Документация

- Swagger UI: http://localhost:8000/api/auth/swagger/
- ReDoc: http://localhost:8000/api/auth/redoc/