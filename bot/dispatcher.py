from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

