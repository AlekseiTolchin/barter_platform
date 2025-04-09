# Платформа для обмена вещами

Монолитное веб-приложение на Django для организации обмена вещами между пользователями.


## Как запустить проект

Скачать удаленный репозиторий выполнив команду

```
git clone https://github.com/AlekseiTolchin/barter_platform
```
Docker и Docker-compose должны быть установлены в системе.

Собрать докер-образы:

```
docker-compose build
```

Запустить докер-контейнеры и не выключать:

```
docker-compose up
```

После запуска веб-сервисов с помощью Docker Сompose в новом терминале, не выключая сайт, загрузить в БД тестовые данные:

```
docker compose exec postgres psql -U admin barter -f /test_data/db_test_data.sql
```
В базе данных создадуться несколько объявлений от разных пользователей. И пользователи:

- admin (superuser) - пароль `admin`
- alex - пароль `alex12345`
- lex - пароль `lex12345`

Накатить миграции с помощью команды:

```
docker compose run --rm web python manage.py migrate
```

Запустить тесты с помощью команды:

```
docker-compose exec web pytest
```

Ссылки для тестирования:

- http://127.0.0.1:8000/admin/ - `админ-панель`
- http://127.0.0.1:8000/api/docs/ - `документация API`  
- http://127.0.0.1:8000/ - `Главная страница`

