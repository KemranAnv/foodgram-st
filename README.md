# Foodgram
## Описание проекта:
Foodgram — сайт, где пользователи могут публиковать рецепты, добавлять их в избранное, подписываться на авторов и создавать список покупок для ингредиентов.

## Технологии
* Python 3.10
* Django 5.2.3
* Django REST Framework
* PostgreSQL
* Docker
* Nginx
* Gunicorn

## Установка и запуск

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/KemranAnv/foodgram-st
    cd foodgram
    ```

2. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    .\venv\Scripts\activate   # Windows
    ```

3. Установите зависимости:
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

4. Создайте файл .env в папке backend с переменными окружения:
    ```
    SECRET_KEY=very-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    POSTGRES_DB=foodgram
    POSTGRES_USER=foodgram_user
    POSTGRES_PASSWORD=foodgram_password
    DB_HOST=db
    DB_PORT=5432
    ```

5. Для локального запуска выполните:
    ```
    python manage.py migrate
    python manage.py runserver
    ```

6. Для запуска в Docker:
    ```
    cd ../infra
    docker-compose up -d
    ```

7. Доступ:

* Фронтенд: http://localhost
* API: http://localhost/api/docs/
* Админ-панель: http://localhost/admin/ (логин: admin@admin.com, пароль: admin)



## Автор
    Annekov Kemran
