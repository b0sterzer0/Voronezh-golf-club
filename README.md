<h1>Сайт гольф-клуба</h1>

<h2>Описание проекта:</h2>
Сайт гольф-клуба. Стек: python, flask, sqlalchemy, postgresql, pytest, docker, html, css, js, jquery, flake8

<h2>Установка:</h2>

1) Склонировать репозиторий
2) Создать окружение
3) pip install -r requirements.txt
4) Создать docker контейнер с образом postgresql не ниже версии 13.x
5) Создать .env и заполнить его по образцу .env.template
6) python commands.py create_db
7) Создать вручную пользователя с параметром is_admin=True
8) python -m pytest -vv
9) Готово

<h2>Запуск:</h2>
python run.py