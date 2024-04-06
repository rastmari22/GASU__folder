from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

class HasReg(BaseFilter):
    def __init__(self,message: Message):
        self.chat_type=message
    async def __call__(self, message:Message):#рабатывает, когда экземпляр класса ChatTypeFilter() вызывают как функцию.
        if isinstance(self.chat_type,str):
            return message.chat.type==self.chat_type
        else:
            return message.chat.type in self.chat_type
