from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes:tuple[int]=(2,)):
    keyboard=InlineKeyboardBuilder()
    for text,data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text,callback_data=data))
    return keyboard.adjust(*sizes).as_markup()

# inline_btn_1 = InlineKeyboardButton(text='Первая кнопка!', callback_data='button1')
# inline_btn_2=InlineKeyboardButton(text='Вторая кнопка', callback_data='btn2')
# inline_kb_full = InlineKeyboardMarkup(inline_keyboard=[[inline_btn_1],[inline_btn_2]])
# inline_btn_3 = InlineKeyboardButton(text='кнопка 3', callback_data='btn3')
# inline_btn_4 = InlineKeyboardButton(text='кнопка 4', callback_data='btn4')
# inline_btn_5 = InlineKeyboardButton(text='кнопка 5', callback_data='btn5')
# # inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
# # inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
# inline_kb_full.insert(InlineKeyboardButton(text="query=''", switch_inline_query=''))
# inline_kb_full.insert(InlineKeyboardButton(text="query='qwerty'", switch_inline_query='qwerty'))
# inline_kb_full.insert(InlineKeyboardButton(text="Inline в этом же чате", switch_inline_query_current_chat='wasd'))

# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# inline_btn_1 = InlineKeyboardButton(text='Первая кнопка!', callback_data='button1')
# inline_btn_2 = InlineKeyboardButton(text='Вторая кнопка', callback_data='btn2')
# inline_kb_full = InlineKeyboardMarkup(inline_keyboard=[[inline_btn_1], [inline_btn_2]])
#
# inline_btn_3 = InlineKeyboardButton(text='кнопка 3', callback_data='btn3')
# inline_btn_4 = InlineKeyboardButton(text='кнопка 4', callback_data='btn4')
# inline_btn_5 = InlineKeyboardButton(text='кнопка 5', callback_data='btn5')
# inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
#
# inline_kb_full.add(InlineKeyboardButton(text="query=''", switch_inline_query=''))
# inline_kb_full.add(InlineKeyboardButton(text="query='qwerty'", switch_inline_query='qwerty'))
# inline_kb_full.add(InlineKeyboardButton(text="Inline в этом же чате", switch_inline_query_current_chat=''))
