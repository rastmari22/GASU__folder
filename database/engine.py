import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from databse.models import Base
from dotenv import find_dotenv,load_dotenv
from databse.orm_query import orm_create_groups
from schedulle.functions import get_groups


async def create_db():
    groups = await get_groups()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with session_maker() as session:
        await orm_create_groups(session, groups)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)