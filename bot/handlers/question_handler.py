from aiogram import types
from aiogram.dispatcher import Dispatcher

from bot.buttons.inline_buttons import questions_and_responses, create_inline_keyboard
from db.database import session
from db.models import Project


async def show_questions(message: types.Message, lang_storage, _):
    locale = lang_storage.get(message.from_user.id, "English 🇺🇸")
    selected_questions = questions_and_responses.get(locale, questions_and_responses["English 🇺🇸"])["questions"]
    inline_keyboard = create_inline_keyboard(selected_questions)
    prompt_message = _("Select Questions") if locale == "English 🇺🇸" else _("Выберите Вопросы:")
    await message.answer(prompt_message, reply_markup=inline_keyboard)


async def handle_question_callback(callback_query: types.CallbackQuery, lang_storage, _):
    locale = lang_storage.get(callback_query.from_user.id, "English 🇺🇸")
    selected_question = callback_query.data.split("_")[1]

    responses = {
        "Which projects do we already have?": lambda: get_projects_response(),
        "Какие проекты у нас уже есть?": lambda: get_projects_response(),
        "Who are we?": "We are ApexBart Company.",
        "Кто мы?": "We are ApexBart Company.",  # Assuming the response is the same for both languages
        "Instructions": "These are instructions.",
        "Инструкция": "These are instructions."  # Assuming the response is the same for both languages
    }

    response = responses.get(selected_question, "No response found.")
    if callable(response):
        response = response()

    await callback_query.message.answer(response)


def get_projects_response():
    projects = session.query(Project).all()
    if projects:
        project_data = [f"Project {i + 1}:\nName:{project.name}\nRequirements:{project.requirements}\n"
                        f"Start date: {project.start_date.strftime('%d:%m:%Y')}\n"
                        for i, project in enumerate(projects)]
        return "\n".join(project_data)
    else:
        return "No projects found."


def setup_question_handler(dp: Dispatcher, lang_storage, _):
    dp.register_message_handler(
        lambda message: show_questions(message, lang_storage, _),
        lambda message: message.text in ['Questions', 'Вопросы']
    )

    dp.register_callback_query_handler(
        lambda query: handle_question_callback(query, lang_storage, _),
        lambda query: query.data.startswith("question_")
    )
