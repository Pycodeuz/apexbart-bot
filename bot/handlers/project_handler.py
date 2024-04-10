import re
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db.database import session
from db.models import Project, Admin
from utils.states import CreateProjectState


async def create_project(callback_query: types.CallbackQuery, state: FSMContext):
    admin_id = callback_query.from_user.id
    admin = session.query(Admin).filter(Admin.tg_id == str(admin_id)).first()

    if admin:
        await CreateProjectState.project_name.set()
        await callback_query.message.answer('Enter project name')
    else:
        await callback_query.message.answer('You do not have permission. You are not Admin')


async def project_name(message: types.Message, state: FSMContext):
    await state.update_data(project_name=message.text)
    await CreateProjectState.next()
    await message.answer("Enter project requirements")


async def project_requirements(message: types.Message, state: FSMContext):
    await state.update_data(requirements=message.text)
    await CreateProjectState.next()
    await message.answer("Enter Start date. for example: %d:%m:%Y")


async def prj_start_date(message: types.Message, state: FSMContext):
    try:
        start_date = datetime.strptime(message.text, "%d:%m:%Y")
        await state.update_data(start_date=start_date)
        await CreateProjectState.next()
        await message.answer("Enter Login codes. for example: 212421, 312411, 632313, ..")
    except ValueError:
        await message.answer("Invalid date format. Please provide the date in the format: day:month:year")
    except Exception as e:
        await message.answer(f"An error occurred: {e}")


async def login_code(message: types.Message, state: FSMContext):
    await state.update_data(login_code=message.text)
    data = await state.get_data()
    if 'login_code' not in data:
        await message.answer('Please provide login codes before proceeding.')
        return
    login_codes = [code.strip() for code in data['login_code'].split(',')]
    if not login_codes:
        await message.answer('Please provide valid login codes before proceeding.')
        return
    await state.update_data(login_codes=login_codes)

    new_project = Project(
        name=data['project_name'],
        requirements=data['requirements'],
        start_date=data['start_date'],
        login_codes=login_codes
    )

    session.add(new_project)
    session.commit()
    await state.finish()
    await message.answer('Project created successfully 🎉')


async def project_list(message: types.Message, lang_storage, _):
    all_projects = session.query(Project).all()

    if not all_projects:
        await message.answer("Project not found 🤷")
        return

    for index, project in enumerate(all_projects, start=1):
        project_details = (
            f"Project № {index}\n"
            f"Name: {project.name}\n"
            f"Requirements: {project.requirements}\n"
            f"Start date: {project.start_date.strftime('%d:%m:%Y')}\n"
            f"Number login codes: {len(project.login_codes)}\n"
        )
        add_login_code_button = InlineKeyboardButton("Add login codes",
                                                     callback_data=f"add_login_code_{project.id}")
        delete_button = InlineKeyboardButton("Delete project", callback_data=f"delete_project_{project.id}")
        keyboard = InlineKeyboardMarkup().row(add_login_code_button, delete_button)
        await message.answer(project_details, reply_markup=keyboard)


async def handle_add_login_codes(callback_query: types.CallbackQuery, state: FSMContext):
    admin = session.query(Admin).filter(Admin.tg_id == str(callback_query.from_user.id)).first()
    if admin:
        project_id_match = re.match(r"add_login_code_(\d+)", callback_query.data)
        if project_id_match:
            project_id = int(project_id_match.group(1))

            await state.update_data(project_id=project_id)

            await callback_query.message.answer("Please send the login codes separated by commas.")

            await state.set_state("waiting_for_login_codes")


async def handle_login_codes_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    project = session.query(Project).get(data.get("project_id"))
    if project:
        all_codes = project.login_codes + message.text.split(',')
        project.login_codes = []
        project.login_codes.extend(all_codes)
        session.commit()
        await message.answer("Login codes have been added to the project.")
    else:
        await message.answer("Project not found 🤷")

    await state.finish()


async def delete_project(callback_query: types.CallbackQuery):
    project_id_match = re.match(r"delete_project_(\d+)", callback_query.data)
    if project_id_match:
        project_id = int(project_id_match.group(1))

        project = session.query(Project).filter(Project.id == project_id).first()

        if project:
            session.delete(project)
            session.commit()
            await callback_query.message.answer(f"Project '{project.name}' has been deleted.")
        else:
            await callback_query.message.answer("Project not found.")
    else:
        await callback_query.message.answer("Invalid callback data.")


def setup_project_handlers(dp: Dispatcher, lang_storage, _):
    dp.register_callback_query_handler(
        create_project,
        lambda callback_query: callback_query.data == "create_project"
    )
    dp.register_message_handler(
        project_name,
        state=CreateProjectState.project_name
    )
    dp.register_message_handler(
        project_requirements,
        state=CreateProjectState.requirements
    )
    dp.register_message_handler(
        prj_start_date,
        state=CreateProjectState.start_date
    )
    dp.register_message_handler(
        login_code,
        state=CreateProjectState.login_code
    )
    dp.register_callback_query_handler(
        handle_add_login_codes,
        lambda callback_query: callback_query.data.startswith("add_login_code_")
    )
    dp.register_callback_query_handler(
        lambda callback_query: project_list(callback_query.message, lang_storage, _),
        lambda callback_query: callback_query.data == "project_list"
    )
    dp.register_callback_query_handler(
        delete_project,
        lambda callback_query: callback_query.data.startswith("delete_project_")
    )
    dp.register_message_handler(
        handle_login_codes_input,
        state="waiting_for_login_codes",
        content_types=types.ContentType.TEXT
    )
