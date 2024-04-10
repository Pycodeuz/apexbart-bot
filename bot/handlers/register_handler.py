import logging  # Add logging module
import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from db.database import session
from db.models import User, Project
from utils.states import RegisterState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def register_user(message: types.Message, state: FSMContext, lang_storage, gettext):
    user_tg_id = str(message.from_user.id)
    selected_language = lang_storage[message.from_user.id]
    user = session.query(User).filter(User.tg_id == user_tg_id).first()

    if user:
        await message.answer(
            gettext("You are already registered.") if selected_language == "English 🇺🇸" else
            gettext("Вы уже зарегистрированы."))
        return

    await RegisterState.full_name.set()
    await message.answer(gettext("Please enter your full name:") if selected_language == "English 🇺🇸" else
                         gettext("Пожалуйста, введите своё полное имя:"))
    logger.info("Register user function called.")


async def process_name(message: types.Message, state: FSMContext, lang_storage, gettext):
    selected_language = lang_storage[message.from_user.id]

    await state.update_data(full_name=message.text)
    await RegisterState.next()

    await message.answer(gettext("Select Project you want to register") if selected_language == "English 🇺🇸" else
                         gettext("Выберите проект, на который вы "
                                 "хотите зарегистрироваться."))

    # Fetch all projects from the database
    projects = session.query(Project).all()

    # Create buttons for each project
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    for project in projects:
        button_text = project.name
        callback_data = f"project_selection_{project.id}"
        keyboard_markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))

    await message.answer(gettext("---"), reply_markup=keyboard_markup)

    logger.info("Process name function called.")


async def project_selection(callback_query: types.CallbackQuery, state: FSMContext, lang_storage, gettext):
    # Print or log callback query data
    print("Callback Query Data:", callback_query.data)

    selected_language = lang_storage[callback_query.from_user.id]
    # Print or log selected language
    print("Selected Language:", selected_language)

    project_id = int(callback_query.data.split("_")[2])
    # Print or log selected project ID
    print("Selected Project ID:", project_id)

    # Fetch the selected project from the database
    selected_project = session.query(Project).filter(Project.id == project_id).first()

    if not selected_project:
        await callback_query.answer(gettext("Invalid project selection. Please select a valid project."))
        return

    # Print or log selected project details if needed
    print("Selected Project Details:", selected_project)

    await state.update_data(user_project=project_id)
    await RegisterState.next()

    await callback_query.message.answer(gettext("Enter your language level") if selected_language == "English 🇺🇸" else
                                        gettext("Пожалуйста, укажите ваш уровень языка: "))
    logger.info("Project selection function called.")


async def process_lang_level(message: types.Message, state: FSMContext, lang_storage, gettext):
    selected_language = lang_storage[message.from_user.id]

    await state.update_data(lang_level=message.text)
    await RegisterState.next()

    used_login_codes = session.query(User.login_code).all()
    all_login_codes = session.query(Project.login_codes).all()

    used_login_codes = [code for row in used_login_codes for code in row[0]]
    all_login_codes = [code for row in all_login_codes for code in row[0]]

    available_login_codes = [code for code in all_login_codes if code not in used_login_codes]

    if not available_login_codes:
        await message.answer(gettext("No more login codes available. Registration failed."))
        await state.finish()
        return

    selected_login_code = random.choice(available_login_codes)

    await state.update_data(login_code=selected_login_code)

    await message.answer(gettext("Registration completed successfully. Your login code is: {login_code}").format(
        login_code=selected_login_code) if selected_language == "English 🇺🇸" else
                         gettext("Регистрация успешно завершена. Ваш код для входа: {login_code}").format(
                             login_code=selected_login_code))

    data = await state.get_data()

    new_user = User(full_name=data['full_name'],
                    tg_id=str(message.from_user.id),
                    lang_level=data['lang_level'],
                    login_code=data['login_code'],
                    project_id=data['user_project'])

    session.add(new_user)
    session.commit()

    await state.finish()
    logger.info("Process language level function called.")

    return new_user


def setup_registration_handler(dp: Dispatcher, lang_storage, gettext):
    dp.register_message_handler(
        lambda message: register_user(message, dp.current_state(), lang_storage, gettext),
        lambda message: message.text in ['Registration', 'Регистрация']
    )
    dp.register_message_handler(
        lambda message: process_name(message, dp.current_state(), lang_storage, gettext),
        state=RegisterState.full_name
    )
    dp.register_callback_query_handler(
        lambda callback_query, state: project_selection(callback_query, state, lang_storage, gettext),
        lambda callback_query: callback_query.data.startswith("project_selection_"),
        state=RegisterState.user_project
    )
    dp.register_message_handler(
        lambda message: process_lang_level(message, dp.current_state(), lang_storage, gettext),
        state=RegisterState.lang_level
    )
    logger.info("Registration handlers set up.")

