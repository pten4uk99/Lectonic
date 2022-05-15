# Lectonic
Проект предоставляет возможность взаимодействия Лекторов и Заказчиков лекций.
Каждый лектор можно легко подобрать место, время, и лекцию, которую он хотел бы провести.
С свою очередь любой заказчик, может найти себе подходящего лектора для проведения нужной ему лекции.

## Quickstart
1. Из корневой директории проекта /Lectonic: <br/>
Активируем виртуальное окружение
```cmd
python -m venv venv
venv/scripts/activate
```
Запуск базы данных и брокера в контейнере:
```cmd
docker-compose up
```
2. Запуск Backend локального сервера:
```cmd
cd speakers
python manage.py makemigrations authapp emailapp chatapp workroomsapp
python manage.py migrate
python manage.py loaddb # Загрузка необходимых данных в базу для коррректной работы
python manage.py runserver
```
3. Запуск Frontend локального сервера с помощью webpack-dev-server:
```cmd
cd ../frontend
yarn install
yarn dev
```
4. Локальный webpack сервер будет доступен по адресу <http://localhost:3000>
<br/>
(В целях демонстрации отключено подтверждение email по почте)