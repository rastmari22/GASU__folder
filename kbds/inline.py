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

start_btns = {"Добавить группу": "add_group", "❓": "help"}
welcome_menu={'❓❗❌✅↩✔🔴🟠🟡🟢🔵🟣🟤⚫🔘🟫🟪🟩🟦🟧🟨🟥⚪'
              '⬛⬜◼◻◾◽▪▫🔶🔸🔷🔺💬💭🗯🕐🕑🕚🕒🕙🕘🕠🕡🕢🕠🕟🕧🕦'
              '🕞🕖🕕🕔🕓🕛🕜🕝🕥🕣🕤🐾👾✍🏽🔒🔐🔑🔍📄📤📁📂🗂💼📝'
              '📌📍🗑✂❤🤍💛🖐🏽🙌🏽✋🏽🖖🏽✌🏽➕➖💲👁‍🗨'}
start_reply_markup=get_callback_btns(btns=start_btns)
back_btn={"↩":f""}
btns = {"➕": "add_group", "❓": "startpoint"}
add_reply_markup=get_callback_btns(btns=start_btns)