## Всі необхідні компоненти для запуску програми:

- Python - https://www.python.org/downloads/
- PyCharm - https://www.jetbrains.com/ru-ru/pycharm/
- Зклонувати проект
- Запустити проект в Pycharm ВСІ КОМАНДИ ВПИСУВАТИ В КОНСОЛІ Pycharm
- Створити віруальне оточення командою - python3 -m venv venv
- Активувати віртуальне оточення командою - myvenv\Scripts\activate в Windows або source myvenv/bin/activate в Mac OS / Linux.
- Стягнути залежності з requirements.txt командою - pip install -r requirements.txt

## Для використання Docker:
- Створіть Docker образ: docker build -t event-test-task .
- Запустіть Docker контейнер: docker run -p 8000:8000 event-test-task

## Налаштуйте email сервер:

- EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
- EMAIL_HOST = 'smtp.your-email-provider.com'
- EMAIL_PORT = 587
- EMAIL_USE_TLS = True
- EMAIL_HOST_USER = 'your-email@example.com'
- EMAIL_HOST_PASSWORD = 'your-password'
- DEFAULT_FROM_EMAIL = 'your-email@example.com'

## Для документації використовував Swagger - http://127.0.0.1:8000/swagger/

## Функціонал

- Реєстрація та аутентифікація користувачів.
- Створення, перегляд, оновлення та видалення подій.
- Реєстрація користувачів на події.
- Фільтрація та пошук подій за заголовком, датою та місцем.
- Надсилання email-повідомлень про реєстрацію на подію.
