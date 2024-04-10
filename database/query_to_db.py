from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Group, association_table


async def has_registration(user_name:str,session: AsyncSession):
    query = select(User).where(User.user_name == user_name)
    result = await session.execute(query)
    return result.first()
async def group_exist(session: AsyncSession,gr_name:str):
    query = select(Group).where(Group.name==gr_name)
    result = await session.execute(query)
    return result.first()

async def connect_user_with_group(session: AsyncSession, group_name: str, username: str):
    user_result = await session.execute(select(User).where(User.user_name == username))
    user = user_result.scalar()

    group_result=await  session.execute(select(Group).where(Group.name==group_name))
    group=group_result.scalar()

    ins = association_table.insert().values(user_id=user.id, group_id=group.id)
    await session.execute(ins)
    await session.commit()