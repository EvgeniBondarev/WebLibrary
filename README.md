<h3>Бондарев Евгений Юрьевич</h3>
<h4>«Библиотека» - автоматизация учета выдачи книг читателям</h4>




Технологический стек для веб-приложения на Python с использованием Django и базы данных SQLite:
1) Язык программирования - Python 3.10
2)  Веб-фреймворк - Django 
3)  База данных - SQLite
4)  Фронтенд - HTML, CSS
5)  Web-сервер - Heroku



Исходные коды приложения расположен в репозитории GitHub - https://github.com/EvgeniBondarev/WebLibrary.git

Приложение расположено по адресу - https://lab1-test-3cf82a9789bc.herokuapp.com/

<br><br>
<h4>Описание работы с системой для пользователя:</h4>
Начальная страница представляет собой форму входа в аккаунт с выбором пользователей из списка. Также есть возможность зарегистрировать нового уникального пользователя, перейдя по ссылке "Регистрация", и просмотреть информацию о выдаче книг всем пользователям. После входа в систему пользователь может выбрать из списка возможностей: получить книгу и вернуть книгу, а также посмотреть историю операций.

<br>
<h4>Описание работы с системой для программиста:</h4>
1.Клонируйте репозиторий на свой локальный компьютер:

     `git clone https://github.com/EvgeniBondarev/WebLibrary.git`


2.Перейдите в каталог проекта:
    `cd ваш-репозиторий`
    
3.Создайте виртуальное окружение и активируйте его:
    
   `venv\Scripts\activate`
    
4.Установите зависимости проекта:

    `pip install -r requirements.txt`
    
5.Выполните миграции базы данных:
    
    `python manage.py migrate`
    
6.Запустите локальный сервер:

    `python manage.py runserver`

<br>
<h4>Базу данных можно скачать по ссылке:</h4>https://github.com/EvgeniBondarev/WebLibrary/raw/main/db.sqlite3

Так же можно использовать DDL запросы:

```sql
CREATE TABLE reader (
    id          INTEGER       NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    last_name   VARCHAR (100) NOT NULL,
    first_name  VARCHAR (100) NOT NULL,
    middle_name VARCHAR (100) NOT NULL
);

```
```sql
CREATE TABLE book (

id INTEGER NOT NULL

PRIMARY KEY AUTOINCREMENT,

title VARCHAR (200) NOT NULL,

author_id BIGINT NOT NULL

REFERENCES author (id) DEFERRABLE INITIALLY DEFERRED,

is_visible BOOL NOT NULL,

code INTEGER UNIQUE

);
```
```sql
CREATE TABLE author (

id INTEGER NOT NULL

PRIMARY KEY AUTOINCREMENT,

first_name VARCHAR (100) NOT NULL,

last_name VARCHAR (100) NOT NULL,

middle_name VARCHAR (100) NOT NULL

);
```
```sql
CREATE TABLE book_loan (

id INTEGER NOT NULL

PRIMARY KEY AUTOINCREMENT,

loan_date DATETIME NOT NULL,

return_date DATETIME,

book_id BIGINT NOT NULL

REFERENCES book (id) DEFERRABLE INITIALLY DEFERRED,

reader_id BIGINT NOT NULL

REFERENCES reader (id) DEFERRABLE INITIALLY DEFERRED

);
```
