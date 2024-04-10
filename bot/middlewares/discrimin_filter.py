import asyncio

from aiogram import types, Dispatcher
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler


class DiscriminationMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        if await self.contains_discrimination(message.text):
            await message.reply("Iltimos, haqoratli so'zlarni ishlatmang!!!")
            raise CancelHandler()

    async def contains_discrimination(self, text: str) -> bool:
        try:
            word_list = [
                
            ]
            if text.lower() in word_list:
                return True
            else:
                return False

        except:
            pass
