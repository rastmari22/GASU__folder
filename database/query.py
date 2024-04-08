from sqlalchemy import select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database.models import  Subject, User, Group, association_table, File


async def orm_add_user(
        session:AsyncSession,
        user_name:str
):
    query=select(User).where(User.user_name==user_name)
    result=await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_name=user_name)
        )
        await session.commit()

async def check_user(session:AsyncSession,user_name:str):
    query=select(User).where(User.user_name==user_name)
    res=await session.execute(query)
    return res.fetchone()

async def is_user_get_group(session:AsyncSession,user_name:str):
    query=select(Group).where(Group.users==user_name)
    result=await session.execute(query)
    return result is not None
async def orm_get_user_by_id(session:AsyncSession,u_d:int):
    query = select(User).where(User.id == u_d)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_userid_by_name(session:AsyncSession,u_n:str):
    query = select(User).where(User.user_name == u_n)
    result = await session.execute(query)
    return result.scalar()
async def orm_connect_user_and_group(session: AsyncSession, group_name: str, username: str):
    # user = await session.execute(select(User).filter_by(user_name=username))
    # user = user.scalar()
    # group = await session.execute(select(Group).filter_by(name=group_name))
    # group = group.scalar()
    # stmt = insert(association_table).values(user_id=user.id, group_id=group.id)
    # stmt = stmt.on_conflict_do_nothing(index_elements=['user_id', 'group_id'])  # учитываем уникальность комбинации
    # await session.execute(stmt)
    # await session.commit()

    result = await session.execute(select(User).where(User.user_name == username))
    user = result.scalar()

    res_gr=await  session.execute(select(Group).where(Group.name==group_name))
    group=res_gr.scalar()



    ins = association_table.insert().values(user_id=user.id, group_id=group.id)

    # Выполнение оператора вставки с помощью асинхронной сессии
    await session.execute(ins)
    await session.commit()

async def get_user_groups(session: AsyncSession, username: str):
    stmt = select(Group).join(association_table).join(User).filter(User.user_name == username)
    result = await session.execute(stmt)
    user_groups = result.scalars().all()
    return user_groups
async def create_users_groups(session:AsyncSession,user_name:str,group_id:int):
    result=await session.execute(select(User).where(User.user_name==user_name))
    user=result.scalar()
    ins = association_table.insert().values(user_id=user.id, group_id=group_id)

    # Выполнение оператора вставки с помощью асинхронной сессии
    await session.execute(ins)
    await session.commit()
    # user_group = association_table(user_id=user_id, group_id=group_id)
    # session.add(user_group)
    # await session.commit()
async def get_users_group(session:AsyncSession,user_name:str):
    user = await orm_get_userid_by_name(session, user_name)  # Получаем пользователя по имени
    stmt = (
        select(association_table).
        where(association_table.c.user_id == user.id)
    )  # Создаем запрос для выборки из таблицы "user_group" по идентификатору пользователя

    result = await session.execute(stmt)
    user_groups = result.scalars().all()
    return user_groups

async def get_user_groups(session:AsyncSession,username:str):
    result = await session.execute(select(User).where(User.user_name == username))
    user = result.scalar()
    if user:
        await session.execute(select(User).where(User.user_name == username).options(selectinload(User.groups)))
        groups = user.groups
        if groups:
            group_names = [group.name for group in groups]
        return groups

async def orm_add_group_for_user(session:AsyncSession,user_id:int,group_name:str):
    user = await session.execute(select(User).where(User.user_id == user_id))
    if user.first() is not None:
        group = Group(name=group_name, user_id=user_id)
        session.add(group)
        await session.commit()

async def orm_add_subject_to_group(session: AsyncSession, group_id: int, subject_name: str):
    group = await session.execute(select(Group).where(Group.id == group_id))
    if group.scalar() is not None:  # используем scalar() для получения первого результата
        subject = Subject(name=subject_name, group_id=group_id)
        session.add(subject)
        await session.commit()


async def orm_get_subjects_in_group(session: AsyncSession, user_id: int, group_id: int):
    subjects = await session.execute(select(Subject).join(Group).join(User).where(User.user_id == user_id, Group.id == group_id))
    return subjects.all()

async def orm_get_group_by_group_name(session:AsyncSession,group_name:str):
    query=select(Group).where(Group.name==group_name)
    result=await session.execute(query)
    return result.scalar()

async def orm_create_groups(session: AsyncSession, groups: list):
    query=select(Group)
    result=await session.execute(query)
    if result.first():
        return
    session.add_all([Group(name=name) for name in groups])
    await session.commit()

async def orm_create_subjects_test(session: AsyncSession,groups:list):
    for group in groups:
        group_name = group  # Assuming the group name is the same as the variable name
        subjects = groups[group]

async def orm_get_groups(session: AsyncSession):
    query = select(Group)
    result = await session.execute(query)
    return result.scalars().all()

async def group_exist(session: AsyncSession,gr_name:str):
    query = select(Group).where(Group.name==gr_name)
    result = await session.execute(query)
    return result.first()
    # return result is not None
async def orm_get_group(session: AsyncSession,gr_name:str):
    query = select(Group).where(Group.name==gr_name)
    result = await session.execute(query)
    return result.scalar()
async def orm_get_group_by_id(session: AsyncSession,gr_id:int):
    query = select(Group).where(Group.id==gr_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_subject_test(session: AsyncSession, subject: str, subject_group_id: int):
    subject_test = await session.execute(
        select(Subjecttest).where(Subjecttest.name == subject, Subjecttest.group_id == subject_group_id))
    return subject_test.scalar()


async def create_group_subjects(session: AsyncSession, group_subject: dict):
    for group, subjects in group_subject.items():
        group_instance = await orm_get_group(session, group)
        group_id = group_instance.id
        for subject in subjects:
            subject_instance = await orm_get_subject_test(session, subject, group_id)
            if not subject_instance:
                subject_instance = Subject(name=subject, group_id=group_id)
                session.add(subject_instance)

            await session.commit()


async def create_group_subjects(session: AsyncSession, group_subject: dict):
    # async with session.begin():
    for group, subjects in group_subject.items():
        group_instance = await orm_get_group(session,group)
        for subject in subjects:
                result = await session.execute(select(Subject).where(and_(Subject.name==subject, Subject.group_id==group_instance.id)))
                subject_instance = result.scalar()

                if not subject_instance:
                    subject_instance = Subject(name=subject, group_id=group_instance.id)
                    session.add(subject_instance)
                    await session.commit()


async def orm_get_subjects_by_group(session: AsyncSession, group_id: int):
    query = select(Subject).where(Subject.group_id == group_id)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_create_file(session:AsyncSession,name:str,subject_id:int,user_id:int):
    file_instance = await orm_get_file(session, name,subject_id,user_id)
    print(file_instance)
    if not file_instance:
        file_instance = File(name=name,subject_id=subject_id,user_id=subject_id)
        session.add(file_instance)
        print('создан',file_instance)
        await session.commit()
async def orm_get_file(session, name, subject_id, user_id):
    stmt =select(File).where(File.name == name).where(File.subject_id == subject_id).where(File.user_id == user_id)
    print('tcnm', stmt)
    result = await session.execute(stmt)
    return result.scalar()
async def orm_get_files_by_subjectid(session, subject_id):
    stmt =select(File).where(File.subject_id == subject_id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def orm_get_files_by_user(session:AsyncSession,user_id:int):
    query = select(File).where(File.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()
async def orm_get_files_by_user_subject(session:AsyncSession,subject_id:int,user_id:int):
    query = select(File).where(File.subject_id == subject_id).where(File.user_id == user_id)
    result = await session.execute(query)
    return result.fetchall()
    # print(stmt)

    # result = await session.execute(stmt)
    # # print(result)
    # return result.scalars().all()
async def orm_get_subject_by_name_and_group_name(session: AsyncSession, subject: str, group_id: int):
    subject_test = (
        select(Subject)
        .where(Subject.name == subject, Subject.group_id == group_id)
    )
    subject_result = await session.execute(subject_test)
    return subject_result.scalar()

async def add_file(session: AsyncSession, name: str, show_name:str,subject_id: int, user_id: int):

    new_file = File(name=name,show_name=show_name, subject_id=subject_id, user_id=user_id)
    session.add(new_file)
    await session.commit()
# async def create_file(session: AsyncSession, name: str, subject_id: int, user_id: int):
#
#     new_file = NewFile(name=name, subject_id=subject_id, user_id=user_id)
#     session.add(new_file)
#     await session.commit()

async def get_user_files_by_subject(session: AsyncSession, user_id: int, subject_id: int):

    stmt = select(File).join(Subject).where(Subject.id == subject_id, File.user_id == user_id)
    files = await session.execute(stmt)
    return files.scalars().all()

async def orm_get_subject_by_name(session: AsyncSession, subject_id: int):
    subject = await session.execute(
        select(Subject).where(Subject.id == subject_id))
    return subject.scalar()

async def get_file_url(session:AsyncSession,file_id:int):
    url=await session.execute(select(File).where(File.id==file_id))
    return url.scalar()

async def delete_file(session:AsyncSession,file:File):
    query=delete(File).where(File.id==file.id)
    await session.execute(query)
    await session.commit()