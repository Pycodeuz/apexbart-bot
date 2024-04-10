from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Language selection buttons
language_selection_buttons = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(
    KeyboardButton('Pусский 🇷🇺')
).add(
    KeyboardButton('English 🇺🇸')
)

# Main menu buttons
main_menu_buttons = {
    "English 🇺🇸": ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    .row(
        KeyboardButton('My Profile'),
        KeyboardButton('Registration'),
        KeyboardButton('Questions')
    ),

    "Pусский 🇷🇺": ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    .row(
        KeyboardButton("Мой Профиль"),
        KeyboardButton('Регистрация'),
        KeyboardButton('Вопросы')
    )
}


# Create phone request keyboard
def create_phone_request_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_request_button = KeyboardButton("Send Phone Number", request_contact=True)
    keyboard.add(phone_request_button)
    return keyboard
