from fastapi import APIRouter, HTTPException
from db import database, table_orders
from models import order
from datetime import datetime
from typing import List

router = APIRouter()


@router.get('/fake_orders/{count}')
async def create_fake_orders(count: int):
    for i in range(count):
        query = table_orders.insert().values(            
            id = i,   
            user_id = i,         
            shop_item_id = i,
            timestamp = datetime.now(),
            is_completed = False
        )
        await database.execute(query)
    return {'message': f'{count} fake orders created'}

@router.get('/orders/', response_model=list[order.ModelOrder])
async def get_all_orders():
    query =  table_orders.select()
    result = await database.fetch_all(query)
    return result

@router.get('/orders/{order_id}', response_model=order.ModelOrder)
async def get_order(order_id: int):
    query =  table_orders.select().where(table_orders.c.id == order_id)
    result = await database.fetch_one(query)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail='Order not found')
    
@router.post("/orders/", response_model=order.ModelOrder)
async def create_order(order: order.ModelOrder):
    query = table_orders.insert().values(    
        user_id = order.user_id,
        shop_item_id = order.shop_item_id,
        timestamp = order.timestamp,
        is_completed = order.is_completed,
    )        
    last_record_id = await database.execute(query)
    return await database.fetch_one(
        table_orders.select()
            .where(table_orders.c.id == last_record_id))

@router.put("/orders/", response_model=order.ModelOrder)
async def update_order(order: order.ModelOrder):
    order_found = await database.fetch_one(
        table_orders.select()
        .where(table_orders.c.id == order.id))
    if order_found:                
        query = table_orders.update() \
                .where(table_orders.c.id == order.id).values(**order.dict())
        await database.execute(query)
        return await database.fetch_one(
        table_orders.select()
            .where(table_orders.c.id == order.id))
    else:
        raise HTTPException(status_code=404, detail='Order not found')

@router.delete("/order/{order_id}")
async def delete_order(order_id: int):
    order_found = await database.fetch_one(
        table_orders.select()
        .where(table_orders.c.id == order_id))
    if order_found:                
        query = table_orders.delete().where(table_orders.c.id == order_id)
        await database.execute(query)
        return {'message': 'User deleted'}
    else:
        raise HTTPException(status_code=404, detail='Order not found')
    
    

