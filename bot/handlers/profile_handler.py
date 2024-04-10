from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from db.database import session
from db.models import User, Project


async def profile_handler(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    user = session.query(User).filter(User.tg_id == user_id).first()

    if not user:
        await message.answer("You are not registered yet.")
        return

    project = session.query(Project).get(user.project_id)
    project_name = project.name if project else 'N/A'

    profile_info = (
        f"Full Name: {user.full_name}\n"
        f"Language Level: {user.lang_level}\n"
        f"Login Code: {user.login_code}\n"
        f"Project: {project_name}\n"
        f"Exam Status: {user.exam_status}\n"
        f"Task Completion: {user.task_completion}"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    toggle_task_button_true = types.InlineKeyboardButton("Mark as Completed",
                                                         callback_data="toggle_task_completion_true")
    toggle_task_button_false = types.InlineKeyboardButton("Mark as Incomplete",
                                                          callback_data="toggle_task_completion_false")
    markup.add(toggle_task_button_true, toggle_task_button_false)

    await message.answer(profile_info, reply_markup=markup)


async def handle_toggle_task_completion_true_callback(query: types.CallbackQuery, state: FSMContext):
    user_id = str(query.from_user.id)
    user = session.query(User).filter(User.tg_id == user_id).first()

    if not user:
        await query.answer("You are not registered yet.", show_alert=True)
        return

    user.task_completion = True
    session.commit()

    await query.answer("Task completion status marked as True.", show_alert=True)


async def handle_toggle_task_completion_false_callback(query: types.CallbackQuery, state: FSMContext):
    user_id = str(query.from_user.id)
    user = session.query(User).filter(User.tg_id == user_id).first()

    if not user:
        await query.answer("You are not registered yet.", show_alert=True)
        return

    user.task_completion = False
    session.commit()

    await query.answer("Task completion status marked as False.", show_alert=True)


def register_profile_handler(dp: Dispatcher, lang_storage):
    dp.register_message_handler(
        lambda message: profile_handler(message, lang_storage),
        lambda message: message.text in ['My Profile', 'Мой Профиль']
    )

    dp.register_callback_query_handler(handle_toggle_task_completion_true_callback, text="toggle_task_completion_true")
    dp.register_callback_query_handler(handle_toggle_task_completion_false_callback,
                                       text="toggle_task_completion_false")
