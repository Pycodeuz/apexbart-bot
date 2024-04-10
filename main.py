import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from dotenv import load_dotenv

from bot.handlers import *
from bot.middlewares.discrimin_filter import DiscriminationMiddleware

load_dotenv('.env')
TOKEN = os.getenv('TOKEN')

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

LANG_STORAGE = {}
I18N_DOMAIN = "mybot"
LOCALES_DIR = "locales"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    dp.middleware.setup(DiscriminationMiddleware())
    i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)

    start_handler.setup_start_handlers(dp, LANG_STORAGE, i18n.gettext)
    lang_handler.setup_lang_handlers(dp, LANG_STORAGE, i18n.gettext)
    question_handler.setup_question_handler(dp, LANG_STORAGE, i18n.gettext)
    register_handler.setup_registration_handler(dp, LANG_STORAGE, i18n.gettext)
    project_handler.setup_project_handlers(dp, LANG_STORAGE, i18n.gettext)
    user_handler.setup_user_handlers(dp, LANG_STORAGE, i18n.gettext)
    profile_handler.register_profile_handler(dp, LANG_STORAGE)
    admin_handler.setup_admin_handlers(dp, LANG_STORAGE, i18n.gettext)

    logger.info("Starting the bot...")
    await dp.start_polling()
    logger.info("Bot has started successfully.")


if __name__ == '__main__':
    asyncio.run(main())
