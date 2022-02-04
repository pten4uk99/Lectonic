# speakers

## Quickstart
Запуск проекта описан на ос windows. Перед работой у вас должны быть установлены на компьютер следующие зависимости: 
```cmd
pip
python 3.*
```
Как правило, при установке python, pip устанавливается автоматически. При установке не забыть поставить галочку: "добавить pip в path". Тем самым, из командной строки должна появиться возможность обращаться к команде "pip". Так же для удобства работы с кодом, можно воспользоваться интегрированной средой разработки(IDE) - PyCharm, VSCode итд... Советую пользоваться именно терминалом IDE, вместо командной строки.

1. После клонирования проекта (git clone) или скачивания архива, из корневой папки проекта нужно установить и активировать вируальное окружение:
```cmd
python -m venv venv
cd venv/Scripts
activate
cd ../..
```
После этого у вас в терминале перед строкой ввода должна появиться приставка (venv), в случае, если вы сделали все правильно.

2. Затем необходимо запросить файл local_settings у одного из бэкенд разработчиков проекта. Этот файл расположить по пути speakers/speakers/speakers - рядом с файлом settings.py

3. Установка зависимостей и миграции (не забудьте, что у вас должно быть активировано виртуальное окружение):
```cmd
pip install -r requirements.txt
cd speakers # переход в папку speakers, которая лежит рядом с файлом frontend.
python manage.py makemigrations # в папке, в которой находитесь (speakers), должен лежать файл manage.py, чтобы данная команда запустилась успешно.
python manage.py makemigrations authapp
python manage.py makemigrations workroomsapp
python manage.py makemigrations emailapp
python manage.py migrate
```
После запуска последней команды у вас должен появиться в текущей папке файл db.sqlite3.

4. Запуск локального сервера:
```cmd
python manage.py runserver
```
Если все прошло хорошо, у вас в терминале появятся такие строки:
```cmd
System check identified no issues (0 silenced).
February 04, 2022 - 10:11:17
Django version 4.0, using settings 'speakers.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
Локальный сервер станет доступен на вашем компьютере по ссылке http://127.0.0.1:8000/. На него можно делать api запросы так же как на веб сервер, например: http://127.0.0.1:8000/api/auth/signup/
