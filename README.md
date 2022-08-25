# Foodgram - сайт 'Продуктовый помощник'

------------
![example workflow](https://github.com/aakozlov85gmail/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
## Описание проекта
Данный проект представляет собой веб-сайт, на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.



------------

## Используемые технологии:
- Python
- Django
- Django REST Framework
- PostgreSQL
- Nginx
- Gunicorn
- Docker

------------

## Установка и запуск проекта
Выполните установку git, docker и docker-compose на сервере
```sh
sudo apt install git docker docker-compose -y
```
Клонируйте репозиторий и перейдите в него в командной строке:
```sh
git clone git@github.com:aakozlov85gmail/foodgram-project-react.git
cd foodgram-project-react
```
Для работы с базой данных перейдите в директорию infra и создайте в ней .env файл с переменными окружения.
Пример заполнения файла есть в папке backend - .env.example

В директории infra отредактируйте файл nginx.conf: в поле server_name укажите IP адрес вашего сервера.
```
server {
  server_tokens off;
  listen 80;
  server_name <SERVER_IP>;
```
Выполните запуск контейнеров
```sh
sudo docker compose up -d
```
После того как контейнеры будут запущены, выполните миграции и сборку статики
```sh
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py collectstatic --no-input
```
Для создания суперпользователя выполните команду:
```sh
sudo docker compose exec backend python manage.py createsuperuser
```
Проверьте доступность проекта по адресу, указанному в конфигурации ```http://<SERVER_IP>```

------------

## Наполнение проекта тестовыми данными
Перейдите в папку backend и поочередно выполните команды:
```sh
sudo docker compose exec -it backend python manage.py shell
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
quit()
sudo docker compose exec backend python manage.py loaddata data.json
```
В базу данных будет подгружен список ингредиентов и несколько рецептов.



Доступ к админ панели:

    | admin@kozlov.ru  |  admin |

------------


## Ссылки
- Тестовый проект размещен по адресу http://51.250.21.181
- Доступ к документации API http://51.250.21.181/api/docs/redoc.html
- Доступ к административной панели сайта http://51.250.21.181/admin

------------


## Автор проекта

Козлов Андрей
студент 31 когорты факультета Python разработки
Yandex Practicum
