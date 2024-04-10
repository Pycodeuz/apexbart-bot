from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_inline_keyboard(selected_questions):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    for question_text in selected_questions:
        button = InlineKeyboardButton(text=question_text, callback_data=f"question_{question_text}")
        inline_keyboard.add(button)
    return inline_keyboard


create_project_button = InlineKeyboardMarkup(row_width=2)

create_project_button.add(
    InlineKeyboardButton(text="Create Project", callback_data="create_project"),
    InlineKeyboardButton(text="User List", callback_data="user_list_button"),
    InlineKeyboardButton(text="Projects List", callback_data="project_list"),
    InlineKeyboardButton(text="Admins", callback_data="admin_list")
)

questions_and_responses = {
    "English 🇺🇸": {
        "questions": [
            "Who are we?",
            "Instructions",
            "Which projects do we already have?"
        ],
        "responses": {
            "Who are we?": "We are the AppendTask company.",
            "Instructions": "Here are the instructions...",
            "Which projects do we already have?": "We have the following projects..."
        }
    },
    "Pусский 🇷🇺": {
        "questions": [
            "Кто мы?",
            "Инструкция",
            "Какие проекты у нас уже есть?"
        ],
        "responses": {
            "Кто мы?": "Мы компания AppendTask.",
            "Инструкция": "Вот инструкции...",
            "Какие проекты у нас уже есть?": "У нас есть следующие проекты..."
        }
    }
}
