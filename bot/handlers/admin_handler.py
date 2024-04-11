from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.database import session
from db.models import Admin
from utils.states import AdminState


async def admin_list(callback_query: types.CallbackQuery):
    message = callback_query.message  # Extracting message from callback query
    admins = session.query(Admin).all()

    if not admins:
        await message.answer("Admin not found 🤷")
        return

    for index, admin in enumerate(admins, start=1):
        all_admins = (
            f"User № {index}\n"
            f"Admin Name: {admin.name}\n"
            f"TG ID: {admin.tg_id}\n"
        )
        keyboard = InlineKeyboardMarkup(row_width=2)
        add_admin = InlineKeyboardButton("Add", callback_data=f"add_admin{admin.id}")
        delete_admin = InlineKeyboardButton("Delete", callback_data=f"delete_admin{admin.id}")
        keyboard.add(add_admin, delete_admin)
        await message.answer(all_admins, reply_markup=keyboard)


async def add_admin(callback_query: types.CallbackQuery, state: FSMContext):
    await AdminState.name.set()
    await callback_query.message.answer("Send name for admin")


async def admin_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await AdminState.next()
    await message.answer("Send tg_id for admin")


async def admin_tg_id(message: types.Message, state: FSMContext):
    await state.update_data(tg_id=message.text)
    data = await state.get_data()
    new_admin = Admin(
        name=data['name'],
        tg_id=data['tg_id']
    )
    session.add(new_admin)
    session.commit()
    await state.finish()
    await message.answer("Admin added successfully 🎉")


async def delete_admin(callback_query: types.CallbackQuery, state: FSMContext):
    admin_id = int(callback_query.data.split("delete_admin")[1])  # Extracting admin ID from callback data
    admin_to_delete = session.query(Admin).filter(Admin.id == admin_id).first()

    if admin_to_delete:
        session.delete(admin_to_delete)
        session.commit()
        await callback_query.message.answer("Admin deleted successfully.")
    else:
        await callback_query.message.answer("Admin not found.")


def setup_admin_handlers(dp: Dispatcher, lang_storage, _):
    dp.register_callback_query_handler(
        admin_list,
        lambda callback_query: callback_query.data == "admin_list"
    )
    dp.register_callback_query_handler(
        add_admin,
        lambda callback_query: callback_query.data.startswith("add_admin"),
        state="*"
    )
    dp.register_message_handler(
        admin_name,
        state=AdminState.name
    )
    dp.register_message_handler(
        admin_tg_id,
        state=AdminState.tg_id
    )
    dp.register_callback_query_handler(
        delete_admin,
        lambda callback_query: callback_query.data.startswith("delete_admin"),
        state="*"
    )
