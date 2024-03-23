from fastapi import APIRouter, HTTPException
from db import database, table_shop_items
from models import shop_item
from typing import List


router = APIRouter()

@router.get('/fake_items/{count}')
async def create_fake_items(count: int):
    for i in range(count):
        query = table_shop_items.insert().values(
            name = f'item_name{i}',
            description = 'Duis ex laborum consectetur consequat laborum id ad incididunt ut enim elit fugiat tempor.',                        
            price = 100/count
            )
        await database.execute(query)
    return {'message': f'{count} fake items created'}

@router.get('/items/', response_model=list[shop_item.ShopItem])
async def get_all_items():
    query =  table_shop_items.select()
    return await database.fetch_all(query)

@router.get('/items/{item_id}', response_model=shop_item.ShopItem)
async def get_item(item_id: int):
    query =  table_shop_items.select().where(table_shop_items.c.id == item_id)
    result = await database.fetch_one(query)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail='Item not found')
    
@router.post("/items/", response_model=shop_item.ShopItem)
async def create_shopping_item(item: shop_item.ShopItem):
    query = table_shop_items.insert().values(
        name = item.name,
        description = item.description,
        price = item.price
    )        
    last_record_id = await database.execute(query)
    return await database.fetch_one(
        table_shop_items.select()
            .where(table_shop_items.c.id == last_record_id)
        )

@router.put("/items/", response_model=shop_item.ShopItem)
async def update_shopping_item(item: shop_item.ShopItem):
    item_found = await database.fetch_one(
        table_shop_items.select()
        .where(table_shop_items.c.id == item.id))
    if item_found:                
        query = table_shop_items.update() \
                .where(table_shop_items.c.id == item.id).values(**item.dict())
        await database.execute(query)
        return await database.fetch_one(
        table_shop_items.select()
            .where(table_shop_items.c.id == item.id))
    else:
        raise HTTPException(status_code=404, detail='Item not found')

@router.delete("/item/{item_id}")
async def delete_item(item_id: int):
    item_found = await database.fetch_one(
        table_shop_items.select()
        .where(table_shop_items.c.id == item_id))
    if item_found:                
        query = table_shop_items.delete().where(table_shop_items.c.id == item_id)
        await database.execute(query)
        return {'message': 'Item deleted'}
    else:
        raise HTTPException(status_code=404, detail='Item not found')
    
    

