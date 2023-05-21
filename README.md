# Тестовое задание:

## Задача 1

* С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, а также инструкции для подключения к ней. 
    * Необходимо обеспечить сохранность данных при рестарте контейнера (то есть - использовать volume-ы для хранения файлов СУБД на хост-машине.
* Реализовать на Python3 веб сервис (с помощью FastAPI или Flask, например), выполняющий следующие функции:
    * В сервисе должно быть реализован POST REST метод, принимающий на вход запросы с содержимым вида {"questions_num": integer}.
После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов.
    * Далее, полученные ответы должны сохраняться в базе данных из п. 1, причем сохранена должна быть как минимум следующая информация (название колонок и типы данный можете выбрать сами, также можете добавлять свои колонки): 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса. В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
    * Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.
* В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисом из п. 2., его настройке и запуску. А также пример запроса к POST API сервиса.
Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAalchemy,  пользоваться аннотацией типов.

## Задача 2

* Необходимо реализовать веб-сервис, выполняющий следующие функции:
    * Создание пользователя;
Для каждого пользователя - сохранение аудиозаписи в формате wav, преобразование её в формат mp3 и запись в базу данных и предоставление ссылки для скачивания аудиозаписи.

### Детализация задачи:

* С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, а также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера (то есть - использовать volume-ы для хранения файлов СУБД на хост-машине.
* Реализовать веб-сервис со следующими REST методами:
* Создание пользователя, POST:
    * Принимает на вход запросы с именем пользователя;
Создаёт в базе данных пользователя заданным именем, так же генерирует уникальный идентификатор пользователя и UUID токен доступа (в виде строки) для данного пользователя;
Возвращает сгенерированные идентификатор пользователя и токен.
    * Добавление аудиозаписи, POST:
Принимает на вход запросы, содержащие уникальный идентификатор пользователя, токен доступа и аудиозапись в формате wav;
Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и сохраняет их в базе данных;
Возвращает URL для скачивания записи вида http://host:port/record?id=id_записи&user=id_пользователя.
    * Доступ к аудиозаписи, GET:
Предоставляет возможность скачать аудиозапись по ссылке из п 2.2.3.
* Для всех сервисов метода должна быть предусмотрена предусмотрена обработка различных ошибок, возникающих при выполнении запроса, с возвращением соответствующего HTTP статуса.
* Модель данных (таблицы, поля) для каждого из заданий можно выбрать по своему усмотрению.
* В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисами из пп. 2. и 3., их настройке и запуску. А также пример запросов к методам сервиса.
Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAlchemy,  пользоваться аннотацией типов.

<h1 align="center">Развертывание проекта</h1>

<h2>Скачать проект</h2>

```
  git@github.com:A-V-tor/task-flaskREST.git
```

```
  cd task-flaskREST
```
<h2> Создать виртуальное окружение и установить зависимости</h2>

```
    python -m venv venv
    source venv/bin/activate
    
```
`python -m pip install -r requirements.txt` </br> </br>
#### Если вы используете poetry

```
    poetry shell
    poetry install
    
```
## ! Для работы второй части задания требуется установка ffmpeg <a href='https://ffmpeg.org/download.html'>скачать можно тут</a>

Для Mac возможна установка через `brew`
Это займет какое-то время (~ 10 минут)

```
    brew install ffmpeg
    
```

Создать файл `.env` со следующими переменными:

   
        POSTGRES_USER
        POSTGRES_PASSWORD
        POSTGRES_DB
        SECRET_KEY
    

Запустить postgresql в докер контейнере

```
   docker-compose up -d
```
Дождаться старта и настройки контейнера и запустить `Flask`

```
    flask --app wsgi run
```

Для остановки контейнера

```
    docker-compose stop
```
**Маршруты**

http://localhost:5000//quiz - получение вопросов викторины </br>
http://localhost:5000//user - создание нового юзера </br>
http://localhost:5000//music-add - добавление композиции </br>
http://localhost:5000//record - скачивание композиции в mp3 формате </br>
http://localhost:5000/swagger-ui - swagger документация </br></br>

Доступ к моделям возможен через админку </br>
http://localhost:5000/admin

## Тесты
```
   pytest --cov
```

<img src="https://github.com/A-V-tor/task-flaskREST/blob/main/tests.png">
