from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    full_name = State()
    user_project = State()
    lang_level = State()
    login_code = State()


class CreateProjectState(StatesGroup):
    project_name = State()
    requirements = State()
    start_date = State()
    login_code = State()


class AdminState(StatesGroup):
    name = State()
    tg_id = State()
