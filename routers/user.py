from fastapi import APIRouter, HTTPException
from db import database, table_users
from models import user
from typing import List


router = APIRouter()

@router.get('/fake_users/{count}')
async def create_fake_users(count: int):
    for i in range(count):
        query = table_users.insert().values(
            name = f'user_name{i}',
            surname = f'surname_{i}',
            email = f'mail_{i}@mail_{i}.com',
            password = f'password_{i}')
        await database.execute(query)
    return {'message': f'{count} fake users created'}

@router.get('/users/', response_model=list[user.ModelUser])
async def get_all_users():
    query =  table_users.select()
    return await database.fetch_all(query)

@router.get('/users/{user_id}', response_model=user.ModelUser)
async def get_user(user_id: int):
    query =  table_users.select().where(table_users.c.id == user_id)
    result = await database.fetch_one(query)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail='User not found')
    
@router.post("/users/", response_model=user.ModelUser)
async def create_user(user: user.ModelUser):
    query = table_users.insert().values(
        name = user.name,
        surname = user.surname,
        email = user.email,
        password = user.password
    )        
    last_record_id = await database.execute(query)
    return await database.fetch_one(
        table_users.select()
            .where(table_users.c.id == last_record_id))

@router.put("/users/", response_model=user.ModelUser)
async def update_user(user: user.ModelUser):
    user_found = await database.fetch_one(
        table_users.select()
        .where(table_users.c.id == user.id))
    if user_found:                
        query = table_users.update() \
                .where(table_users.c.id == user.id).values(**user.dict())
        await database.execute(query)
        return await database.fetch_one(
        table_users.select()
            .where(table_users.c.id == user.id))
    else:
        raise HTTPException(status_code=404, detail='User not found')

@router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    user_found = await database.fetch_one(
        table_users.select()
        .where(table_users.c.id == user_id))
    if user_found:                
        query = table_users.delete().where(table_users.c.id == user_id)
        await database.execute(query)
        return {'message': 'User deleted'}
    else:
        raise HTTPException(status_code=404, detail='User not found')
    
    

