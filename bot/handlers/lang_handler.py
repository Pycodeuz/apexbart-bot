from aiogram import types
from aiogram.dispatcher import Dispatcher

from bot.buttons.keyboard_buttons import main_menu_buttons
from language import LANGS, find_language, languages


async def choose_language(message: types.Message, lang_storage, _):
    lang = message.text
    locale = lang

    if lang not in LANGS:
        return await message.answer(_("This language is not available. Use en or ru"))

    lang_storage[message.from_user.id] = lang
    selected_language_buttons = main_menu_buttons[lang]
    await message.answer(languages[find_language(locale)][locale]['start'], reply_markup=selected_language_buttons)


def setup_lang_handlers(dp: Dispatcher, lang_storage, _):
    dp.register_message_handler(
        lambda message: choose_language(message, lang_storage, _),
        lambda message: message.text in LANGS
    )
