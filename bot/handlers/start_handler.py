from aiogram import types
from aiogram.dispatcher import Dispatcher

from bot.buttons.inline_buttons import create_project_button  # Import the create_project_button
from bot.buttons.keyboard_buttons import language_selection_buttons
from db.database import session
from db.models import Admin


async def start_command(message: types.Message, lang_storage, _):
    admin = session.query(Admin).filter(Admin.tg_id == str(message.from_user.id)).first()
    if admin:
        await message.answer('Welcome to Admin dashboard',
                             reply_markup=create_project_button)
    else:
        await message.answer('Select your language:', reply_markup=language_selection_buttons)


def setup_start_handlers(dp: Dispatcher, lang_storage, _):
    dp.register_message_handler(
        lambda message: start_command(message, lang_storage, _),
        commands="start"
    )
