# API_Yamdb

Описание:

## Проект YaMDB - это API социальной сети, она собирает оценки и отзывы пользователей на различные произведения.

### Технологии

* Django, 
* djangorestframework,
* djangorestframework_simplejwt

### Запуск dev-сервера:

Клонировать репозиторий,
Установите и активируйте виртуальное окружение,
Установите зависимости из файла requirements.txt

Перейдите в каталог с файлом manage.py выполните команды:
python manage.py migrate,
python manage.py createsuperuser

Запустить проект:
python manage.py runserver

### Документация после запуска dev-сервера находится по адресу  http://127.0.0.1:8000/redoc/
### Доступные эндпоинты:

- api/v1/auth/signup/ - Авторизация
- api/v1/auth/token/ - Получение JWT-токена
- api/v1/users/ - Пользователи
- api/v1/users/me/ - Профиль
- api/v1/categories/ -  Категории произведений
- api/v1/genres/ - Жанры произведений
- api/v1/titles/ - Произведения, к которым пишут отзывы
- api/v1/titles/{title_id}/reviews - Oтзывы
- api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Комментарии к отзывам
