### ОПИСАНИЕ

В проекте реализован блог с публикациями yatube при помощи DRF.
При помощи API можно:
- создать и отредактировать или удалить публикации;
- получить одну публикацию или их список;
- создать и отредактировать или удалить комментарии;
- получить все комментарии под постом или отдельно один комментарий;
- получить список групп или отдельно одну группу;
- подписаться на пользователя;
- получить список своих подписок;

Редактировать и удалять можно только созданную пользователем информацию.
Помимо этого в проекте реализована работа с JWT-токенами.

### КАК ЗАПУСТИТЬ ПРОЕКТ

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com/Kosty-a/api_final_yatube.git
```

```
cd api_final_yatube
```

Создать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### ПРИМЕРЫ ЗАПРОСОВ К API

POST http://127.0.0.1:8000/api/v1/jwt/create/
Content-Type: application/json

{
    "username": "user_3",
    "password": "user_3"
}

POST http://127.0.0.1:8000/api/v1/posts/
Authorization: Bearer <Token>
Content-Type: application/json

{
    "text": "text",
    "group": 3
}

GET http://127.0.0.1:8000/api/v1/follow/?search=user_2
Authorization: Bearer <Token>
