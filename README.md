## Описание проекта

  **QRKot** - это приложение для Благотворительного фонда поддержки котиков.  
  Фонд собирает пожертвования на различные целевые проекты: на медицинское
  обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале,
  на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.  
  С помощью API можно создавать проекты пожертвований с названием, описанием и целевой суммой. Пожертвования направляются в первый открытый проект и когда он закрывается, переходят к следующему. 

## Инструкция по развёртыванию проекта

* клонировать проект на компьютер `git clone https://github.com/OvcharukDmitrij/cat_charity_fund`
* создание виртуального окружения `python -m venv venv`
* запуск виртуального окружения `. venv/Scripts/activate`
* установить зависимости из файла requirements.txt `pip install -r requirements.txt`
* запуск сервера `uvicorn app.main:app --reload`
* инициализируем Alembic в проекте `alembic init --template async alembic`
* создание файла миграции `alembic revision --autogenerate -m "migration_name"`
* применение миграций `alembic upgrade head`
* отмена миграций `alembic downgrade`


## Примеры запросов

  После развёртывания проекта документацию можно найти на эндпоинте `.../docs/`

  POST - запрос для создания проекта пожертвования:
```
{
"name": "string",
"description": "string",
"full_amount": 0
}
```
  Ответ в случае удачного создания проекта:
```
{
"name": "string",
"description": "string",
"full_amount": 0,
"id": 0,
"invested_amount": 0,
"fully_invested": true,
"create_date": "2019-08-24T14:15:22Z",
"close_date": "2019-08-24T14:15:22Z"
}
```
  POST - запрос для создания пожертвования:

```
{
"full_amount": 0,
"comment": "string"
}
```
  Ответ в случае удачного создания пожертвования:

```
{
"full_amount": 0,
"comment": "string",
"id": 0,
"create_date": "2019-08-24T14:15:22Z"
}
```


## Технологии
- `Python 3.9`
- `FastAPI`
- `FastAPI-users`
- `SQLAlchemy`
- `Pydantic`
- `Asyncio`

## Автор

Студент когорты 17+ курса Python-разработчик **Овчарук Дмитрий**