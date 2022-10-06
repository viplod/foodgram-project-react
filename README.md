![API for YaMDB](https://github.com/viplod/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)

Проект размещается по адресу http://viplod.sytes.net/
Для просмотра функционала админки сайта viplod@yandex.ru:123

# Проект Foodgram - продуктовый помощник

## Cтек технологий:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

## Описание проекта
Сервис Foodgram - это продуктовый помощник, который создан для тех кто любит готовить и готов поделиться рецептами с другими. Гости сервиса могут просматривать рецепты, а после регистрации пользователи смогут создавать собственный рецепты, подписываться на других пользователей, добавлять понравившиеся рецепты в избранное и создавать список покупок, по выбранным рецептам.

Проект разворачивается в Docker контейнерах: backend-приложение API, PostgreSQL-база данных, nginx-сервер и frontend-контейнер.

Реализовано CI и CD проекта. При пуше изменений в главную ветку проект автоматические тестируется на соотвествие требованиям PEP8. После успешного прохождения тестов, на git-платформе собирается образ backend-контейнера Docker и автоматически размещается в облачном хранилище DockerHub. Размещенный образ автоматически разворачивается на боевом сервере вмете с контейнером веб-сервера nginx и базой данных PostgreSQL.

## Как запустить проект

Клонируйте репозиторий, переходите в папку, создайте виртуальное окружение, установить docker и docker-compose
```
git clone https://github.com/viplod/foodgram-project-react.git
```

Создать файл окружения и заполнить необходимыми параметрами

```
touch .env
echo DB_ENGINE=django.db.backends.postgresql >> .env
echo DB_NAME=postgres >> .env
echo POSTGRES_PASSWORD=postgres >> .env
echo POSTGRES_USER=postgres  >> .env
echo DB_HOST=db  >> .env
echo DB_PORT=5432  >> .env
echo SECRET_KEY=************ >> .env
```
вместо * необходимо указать секретный ключ django из settings

Установить и запустить приложения в контейнерах:
```
cd infra
docker-compose up -d
```

Запустить миграции, создать суперюзера, собрать статику и заполнить БД ингредиентами:
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --no-input 
docker-compose exec backend python manage.py initdata
```
