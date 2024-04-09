import asyncio
import kbds
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Router, F, types, Bot
from aiogram.filters import Command, StateFilter, CommandStart, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.query import get_user_groups, orm_connect_user_and_group, orm_get_group, group_exist, \
    orm_get_group_by_id, orm_get_subjects_by_group, create_group_subjects, orm_get_userid_by_name, \
    orm_get_subject_by_name_and_group_name, add_file, orm_get_subject_by_name, get_user_files_by_subject, \
    orm_get_group_by_group_name, get_file_url, delete_file
from filters.chat_type import ChatTypeFilter
from kbds.inline import get_callback_btns, btns
from schedulle.functions import get_subjects, get_current_subject

router = Router()
router.message.filter(ChatTypeFilter(["private"]))

from database import query


class AddGroupStates(StatesGroup):

    choosing_group = State()
    choosing_subject = State()

    sending_file_from_group = State()
    sending_file_from_subject = State()

    in_file = State()



@router.message(CommandStart())
async def cmd_start(data: Message | CallbackQuery, session: AsyncSession):

    if isinstance(data, Message):
        user_name = data.chat.username
        await query.orm_add_user(session, user_name)
        await data.answer(
            text="Добро пожаловать в <b>GASUfolder!</b>"
                 "\n\nЭто бот - твой помощник для сохранения файлов.\n\n"
                 "Укажи свою группу и присылай файлы, а бот сам опредлит к "
                 "какому предмет его прикрепить, если ты спешишь и не успеваешь сделать это сам!"
                 "\n\nНажми ❓ под сообщением, чтобы узнать больше о его способностях"
                 "",
            reply_markup=kbds.inline.start_reply_markup
        )
    else:
        await data.message.edit_text(
            text="Добро пожаловать в <strong>GASUfolder!</strong>",
            reply_markup=kbds.inline.start_reply_markup
        )
        await data.answer()



@router.callback_query(F.data == "my_group")
async def show_my_groups(callback: types.CallbackQuery, session: AsyncSession, state: FSMContext):

    username = callback.message.chat.username

    await state.clear()

    user_groups = await get_user_groups(session, username)

    # btns = {"Добавить": "add", "Назад": "startpoint"}

    if user_groups:
        btns.update({user_group.name: f'group_{user_group.id}' for user_group in user_groups})

    await callback.message.edit_text("Мои группы",
                                     reply_markup=get_callback_btns(btns=btns,sizes=(2,1)))

    await state.set_state(AddGroupStates.choosing_group)
    await callback.answer()

@router.callback_query(F.data == 'add')
async def enter_group_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(AddGroupStates.choosing_group)

    msg_id = callback.message.message_id

    await state.update_data(choosing_group=msg_id)

    await callback.message.edit_text(
        "Введите название группы",reply_markup=get_callback_btns(btns={"отмена": "my_group"}))


@router.message(AddGroupStates.choosing_group, F.text)
async def add_group_name(message: Message, session: AsyncSession, state: FSMContext):
    new_group_name = message.text
    username = message.chat.username

    exist_group = await group_exist(session, gr_name=new_group_name)

    if exist_group:

        await orm_connect_user_and_group(session, new_group_name, username)

        user_groups = await get_user_groups(session, username)

        text = "Мои группы"
        add_and_help = {"Добавить": "add", "help me": "back"}
        btns = add_and_help
        btns.update({user_group.name: f'group_{user_group.id}' for user_group in user_groups})

        data_fsm = await state.get_data()

        msg_id = data_fsm['choosing_group']

        await state.clear()
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text=text,
            reply_markup=get_callback_btns(btns=btns)
        )
        await message.delete()
    else:
        btns = {"Отмена": "my_group"}
        text = "Такой группы не существует"
        data_fsm = await state.get_data()
        msg_id = data_fsm['choosing_group']

        await message.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)

        sent_message = await message.answer(
            text=text,
            reply_markup=get_callback_btns(btns=btns)
        )
        sent_message_id = sent_message.message_id
        await state.update_data(choosing_group=sent_message_id)
        await message.delete()
        return


@router.callback_query(or_f(F.data.startswith('group_'), F.data.startswith("back_from_file")))
async def choose_group(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    group_id = int(callback.data.split('_')[1])
    await state.set_state(AddGroupStates.sending_file_from_group)

    group = await orm_get_group_by_id(session, group_id)
    subjects =await get_subjects(group.name)
    await create_group_subjects(session, {group.name: subjects})
    subjects_obj = await orm_get_subjects_by_group(session, group.id)
    await state.update_data(sending_file_from_group=(callback.message.message_id, group.name))

    # subjects.add('Общая')

    btns = {subject.name: f'subject_{subject.id}' for subject in subjects_obj}
    btns['Назад'] = 'my_group'
    await callback.message.edit_text(
            f"{group.name}",
            reply_markup=get_callback_btns(btns=btns,sizes=(1,))
        )
    await callback.answer()


@router.message(AddGroupStates.sending_file_from_group, or_f(F.document, F.photo))
async def process_file_from_group(message: Message, state: FSMContext, session: AsyncSession):
    username = message.from_user.username
    user_obj = await orm_get_userid_by_name(session, username)

    state_data = await state.get_data()
    id_msg_with_group_name, gr_name = state_data["sending_file_from_group"]
    print(id_msg_with_group_name, gr_name)

    current_subject = get_current_subject(gr_name)
    print(current_subject)
    group = await orm_get_group_by_group_name(session, gr_name)
    subject = await orm_get_subject_by_name_and_group_name(session, current_subject, group.id)
    print(subject)
    # message.document.
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        await add_file(session, file_id, file_name, subject.id, user_obj.id)

        chat_id = message.chat.id
        new_msg = await message.answer(f"Файл был добавлен в папку \n{current_subject}")
        message_id = new_msg.message_id

    await asyncio.sleep(1)
    await message.delete()
    await message.bot.delete_message(chat_id, message_id)

@router.callback_query(or_f(F.data.startswith(f'subject_')))
async def choose_subject(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    subject_id = int(callback.data.split('_')[1])

    username = callback.from_user.username
    user_obj = await orm_get_userid_by_name(session, username)

    state_data = await state.get_data()
    id_msg_with_group_name, gr_name = state_data["sending_file_from_group"]

    group = await orm_get_group(session, gr_name)

    await state.set_state(AddGroupStates.sending_file_from_subject)

    subj = await orm_get_subject_by_name(session, subject_id)

    if callback.message.document:
        file, m_id = state_data['infile']
        await delete_file(session, file)

    files_obj = await get_user_files_by_subject(session, user_obj.id, subject_id)
    btns = {}

    btns['Назад'] = f'group_{group.id}'
    if files_obj:
        btns = {f'{f.show_name}': f'file_{f.id}' for f in files_obj}
        btns['Назад'] = f'group_{group.id}'
        if callback.message.document:
            sent_message = await m_id.edit_reply_markup(
                reply_markup=get_callback_btns(btns=btns)
            )
            await callback.message.delete()
        else:
            sent_message = await callback.message.edit_text(
                f"{subj.name}",
                reply_markup=get_callback_btns(btns=btns)
            )
        msg_id = sent_message.message_id
    else:
        if callback.message.document:
            sent_message = await m_id.edit_text(
                text=f" {subj.name}\nНет файлов",
                reply_markup=get_callback_btns(btns=btns)
            )
            await callback.message.delete()
        else:
            sent_message = await callback.message.edit_text(text=f" {subj.name}\nНет файлов",
                                                            reply_markup=get_callback_btns(btns=btns)
                                                            )

    sent_message_id = sent_message
    await state.update_data(sending_file_from_subject=(sent_message, subj, group.id))

@router.message(AddGroupStates.sending_file_from_subject, or_f(F.document, F.photo))
async def process_file_from_group(message: Message, state: FSMContext, session: AsyncSession):
    username = message.from_user.username
    user_obj = await orm_get_userid_by_name(session, username)

    state_data = await state.get_data()
    msg_with_subject_name, current_subject, gr = state_data["sending_file_from_subject"]

    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        await add_file(session, file_id, file_name, current_subject.id, user_obj.id)
        # await
        chat_id = message.chat.id
        new_msg = await message.answer(f"Файл был добавлен в папку \n{current_subject.name}")
        message_id = new_msg.message_id

        # await msg_with_subject_name.edit_text(text=current_subject)

        files_obj = await get_user_files_by_subject(session, user_obj.id, current_subject.id)
        btns = {}

        btns['Назад'] = f'group_{gr}'
        if files_obj:
            btns = {f'{f.show_name}': f'file_{f.id}' for f in files_obj}
            btns['Назад'] = f'group_{gr}'
            await msg_with_subject_name.edit_text(
                f"{current_subject.name}",
                reply_markup=get_callback_btns(btns=btns)
            )

        # await message.answer(text=current_subject.name,reply_markup=get_callback_btns(btns=))
        await asyncio.sleep(1)
        await message.delete()
        await message.bot.delete_message(chat_id, message_id)

@router.callback_query(F.data.startswith('file_'))
async def send_file_to_user(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    file_id = int(callback.data.split('_')[1])

    file_obj = await get_file_url(session, file_id)

    # btns_for_file={"Назад":f'group_{group.id}'}
    state_data = await state.get_data()
    msg_with_subject_name, current_subject, gr = state_data["sending_file_from_subject"]

    btn_file = {"Удалить файл": f"subject_{current_subject.id}", "Скрыть": "hide_file_message"}

    await state.set_state(AddGroupStates.in_file)

    # await callback.message.edit_reply_markup(
    #     reply_markup=get_callback_btns(btns=btns_for_file)
    # )
    m_id = callback.message
    msg_with_file = await callback.message.answer_document(
        document=file_obj.name,
        reply_markup=get_callback_btns(btns=btn_file)
    )
    await state.update_data(infile=(file_obj, m_id))
    await callback.answer()
    # await callback.message.se


@router.callback_query(F.data.startswith("delete_file"))
async def back_to_subject_from_file(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    state_data = await state.get_data()

    id_msg_with_group_name, gr_name = state_data["sending_file_from_group"]
    group = await orm_get_group(session, gr_name)

    msg_with_subject_name, current_subject, gr = state_data["sending_file_from_subject"]

    file, m_id = state_data['infile']
    await delete_file(session, file)
    await callback.message.delete()
