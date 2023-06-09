# Friends

Сервис друзей социальной сети

## Реализованные фичи
 - Регистрация
 - Авторизация
 - Добавление в друзья
 - Удаление из друзей
 - Просмотр списка друзей
 - Просмотр входящих/исходящих заявок в друзья
 - Принятие/отклонение заявок
 - Получить статус дружбы (нет ничего / есть исходящая заявка / есть входящая заявка / уже друзья)

## Технические детали
Некоторые условия работы логики:
- если пользователь1 отправляет заявку в друзья пользователю2, а пользователь2 отправляет заявку пользователю1, то они автоматом становятся друзьями, их заявки автоматом принимаются 
- если пользователь1 отклоняет заявку в друзья от пользователя2, то пользователь2 не может больше отправлять заявки в друзья пользователю1 
- если пользователь1 удаляет из друзей пользователя2, то их "дружба" автоматом прекращается, и пользователь2 не может больше отправлять заявки в друзья пользователю1, и пользователь1 автоматически удаляется из друзей пользователя2

## Как запускать сервис
Сервис упакован в докер контейнер, и приложен docker-compose.yaml поэтому сервис можно запустить командой:
```shell
docker-compose up -d
```

Также автоматически создаются два тестовых пользователя
```json
{
  "username": "test_user1",
  "password": "testuserpassword1"
}

{
  "username": "test_user2",
  "password": "testuserpassword2"
}
```

## Как запускать тесты
```shell
docker-compose exec web ./manage.py test
```

## Примеры использования API

OpenApi спецификация автоматически генерируется и находится в файле schema.yaml

1. **Регистрация**
```shell
curl --location 'http://localhost:8000/users/sign_up' \
--header 'Content-Type: application/json' \
--data '{
    "username":"test",
    "password":"pass",
    "password2":"pass"
}'
```
Ответ:
```json
{
  "id": 1,
  "username": "test"
}
```

2. **Авторизация**
```shell
curl --location 'http://localhost:8000/token/' \
--header 'Content-Type: application/json' \
--data '{
    "username":"test",
    "password":"pass"
}'
```
Ответ:
```json
{
  "refresh": "someRefreshToken",
  "access": "someAccessToken"
}
```

3. **Получить список друзей**
```shell
curl --location 'http://localhost:8000//users/friends/' \
--header 'Authorization: Bearer <InsertToken>'
```
Ответ:
```json
{
  "count": 2,
  "next": null,
  "previous": 0,
  "results": [
      {
        "id": 2,
        "username": "friendName2"
      },
      {
        "id": 3,
        "username": "friendName3"
      }
  ]
}
```