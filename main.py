# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
# — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
# — Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
# — Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.

# • Таблица пользователей должна содержать следующие поля: 
#       id (PRIMARY KEY), 
#       имя, 
#       фамилия, 
#       адрес электронной почты и 
#       пароль.

# • Таблица заказов должна содержать следующие поля:
#       id (PRIMARY KEY), 
#       id пользователя (FOREIGN KEY), 
#       id товара (FOREIGN KEY), 
#       дата заказа и 
#       статус заказа.

# • Таблица товаров должна содержать следующие поля: 
#       id (PRIMARY KEY), 
#       название, 
#       описание
#       цена.

# Создайте модели pydantic для получения новых данных и возврата 
# существующих в БД для каждой из трёх таблиц.

# Реализуйте CRUD операции для каждой из таблиц через 
# создание маршрутов, REST API.

from fastapi import FastAPI, HTTPException

from db import database
from routers import shop_item, user, order

tags_metadata = [
    {"name": "shopping_item", "description": "Товары"},
    {"name": "user", "description": "Пользователи"},
    {"name": "order", "description": "Заказы"}    
]


app = FastAPI(openapi_tags=tags_metadata)

app.include_router(shop_item.router, tags=["shopping_item"])
app.include_router(user.router, tags=["user"])
app.include_router(order.router, tags=["order"])


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


