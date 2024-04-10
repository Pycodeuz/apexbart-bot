from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.database import session
from db.models import User, ExamStatus, Project


async def user_list(message: types.Message, lang_storage, _):
    all_users = session.query(User).all()

    if not all_users:
        await message.answer("User not found 🤷")
        return

    for index, user_db in enumerate(all_users, start=1):
        project = session.query(Project).get(user_db.project_id)
        project_name = project.name if project else 'N/A'

        user_details = (
            f"User № {index}\n"
            f"Full Name: {user_db.full_name}\n"
            f"TG ID: {user_db.tg_id}\n"
            f"Lang Level: {user_db.lang_level}\n"
            f"Login Code: {user_db.login_code}\n"
            f"ExamStatus: {user_db.exam_status}\n"
            f"Project: {project_name}\n\n"
        )
        keyboard = InlineKeyboardMarkup(row_width=2)
        pass_button = InlineKeyboardButton("Pass", callback_data=f"pass_exam_{user_db.id}")
        fail_button = InlineKeyboardButton("Fail", callback_data=f"fail_exam_{user_db.id}")
        keyboard.add(pass_button, fail_button)

        await message.answer(user_details, reply_markup=keyboard)


async def pass_exam(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])
    user = session.query(User).get(user_id)
    if user:
        user.exam_status = ExamStatus.PASSED  # Set to PASSED enum value
        session.commit()
        await callback_query.message.edit_text(f"{callback_query.message.text}\nExam marked as passed ✅")
    else:
        await callback_query.message.edit_text("User not found 🤷")


async def fail_exam(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])
    user = session.query(User).get(user_id)
    if user:
        user.exam_status = ExamStatus.FAILED  # Set to FAILED enum value
        session.commit()
        await callback_query.message.edit_text(f"{callback_query.message.text}\nExam marked as failed ❌")
    else:
        await callback_query.message.edit_text("User not found 🤷")


def setup_user_handlers(dp: Dispatcher, lang_storage, _):
    dp.register_callback_query_handler(
        lambda callback_query: user_list(callback_query.message, lang_storage, _),
        lambda callback_query: callback_query.data == "user_list_button"
    )
    dp.register_callback_query_handler(pass_exam, lambda callback_query: callback_query.data.startswith("pass_exam"))
    dp.register_callback_query_handler(fail_exam, lambda callback_query: callback_query.data.startswith("fail_exam"))
