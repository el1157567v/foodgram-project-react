# FOODGRAM
# Дипломный проект Яндекс.Практикум

---
## Описание приложения
Foodgram («Продуктовый помощник») - это сайт, на котором вы можете добавлять свои рецепты, просматривать рецепты других пользователей, подписываться на foodgram-блоги других авторов, добавлять рецепты в избранное и в корзину покупок. Из корзины покупок вы можете выгрузить список покупок, составленный из продуктов выбранных вами рецептов. И вам больше не придется  вспоминать, что же нужно было докупить для приготовления понравившихся вам рецептов.

---
## Технологии
* Python 3.9.10
* Django 3.2.3
* Django Rest Framework 3.12.4

---
## API Foodgram

### Регистрация пользователя:

Для добавления нового пользователя отправьте POST-запрос на эндпоинт ```/api/users/``` со следующими полями (пример):

```sh
{
"email": "vpupkin@yandex.ru",
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин",
"password": "Qwerty123"
}
```

Для получения авторизационного токена отправьте POST-запрос на эндпоинт:```/api/auth/token/login/``` со следующими полями (пример):

```sh
{
"password": "Qwerty123",
"email": "vpupkin@yandex.ru"
}
```

### Изменение пароля текущего пользователя:

Для изменения пароля отправьте POST-запрос на эндпоинт:```/api/users/set_password/``` со следующими полями (пример):

```sh
{
  "new_password": "string",
  "current_password": "string"
}
```

### Создание нового рецепта:

Для создания нового рецепта отправьте POST-запрос на эндпоинт ```/api/recipes/``` со следующими полями (пример):

```sh
{
"ingredients": [
{
"id": 1123,
"amount": 10
}
],
"tags": [
1,
2
],
"image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
"name": "string",
"text": "string",
"cooking_time": 1
}
```

### Добавление рецепта в избранное или в корзину покупок:

Для добавления рецепта в избранное или в корзину покупок отправьте POST-запрос на эндпоинт ```/api/recipes/{id}/favorite/``` или ```/api/recipes/{id}/shopping_cart/```. Поля для запроса заполнять не нужно, действия производятся по id из эндпоинта.

В ответ на запрос поступит информация следующего содержания(пример): 

```sh
{
"id": 0,
"name": "string",
"image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
"cooking_time": 1
}
```

### Подписка на автора:

Для того, чтобы подписаться на любимого автора, отправьте POST-запрос на эндпоинт ```/api/users/{id}/subscribe/```. Поля для запроса заполнять не нужно, действия производятся по id из эндпоинта.

В ответ на запрос поступит информация следующего содержания (пример): 

```sh
{
"email": "user@example.com",
"id": 0,
"username": "string",
"first_name": "Вася",
"last_name": "Пупкин",
"is_subscribed": true,
"recipes": [
{
"id": 0,
"name": "string",
"image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
"cooking_time": 1
}
],
"recipes_count": 0
}
```

### Получение информации в режиме чтения:

Для получения информации в режиме чтения (GET-запрос) доступны следующие эндпоинты:

```sh
/api/users/- список всех пользователей.
/api/tags/- список всех тегов.
/api/tags/{id}/ - просмотр тега по ID.
/api/recipes/- список всех рецептов.
/api/recipes/{id}/ - просмотр рецепта по ID.
/api/users/subscriptions/ - список всех авторов с их рецептами, на которых вы подписаны.
/api/ingredients/ - список ингредиентов.
/api/ingredients/{id}/ - просмотр ингредиента по ID.
```


---
## Автор

Ведерникова Елена 
Python-разработчик
