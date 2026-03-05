from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.fsm_states import AdminLogin
from config import ADMIN_PASSWORD
from keyboards.admin_kb import admin_panel

router = Router()

@router.message(F.text == "/admin")
async def admin_login(message: Message, state: FSMContext):
    await message.answer("Введите пароль для доступа к админ панели:")
    await state.set_state(AdminLogin.waiting_for_password)

@router.message(AdminLogin.waiting_for_password)
async def check_admin_password(message: Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        await message.answer("Добро пожаловать в админ панель!", reply_markup=admin_panel)
        await state.clear()
    else:
        await message.answer("Неверный пароль. Попробуйте снова.")

@router.message(F.text == "Выйти из админ панели")
async def exit_admin_panel(message: Message):
    await message.answer("Вы вышли из админ панели.", reply_markup=None)

@router.message(F.text == "Управление пользователями")
async def manage_users(message: Message):
    await message.answer("Здесь вы можете управлять пользователями. (Функция в разработке)")

@router.message(F.text == "Управление контентом")
async def manage_content(message: Message):
    await message.answer("Здесь вы можете управлять контентом. (Функция в разработке)")

@router.message(F.text == "Статистика")
async def view_statistics(message: Message):
    await message.answer("Здесь вы можете просматривать статистику. (Функция в разработке)")

@router.message(F.text == "Настройки")
async def view_settings(message: Message):
    await message.answer("Здесь вы можете изменять настройки. (Функция в разработке)")

@router.message()
async def handle_unknown_admin_command(message: Message):
    await message.answer("Неизвестная команда. Пожалуйста, выберите действие из админ панели.") 


@router.message(F.text == "Users")
async def show_users(message: Message, session):
    users = await session.execute("SELECT telegram_id, full_name, role FROM users")
    result = users.fetchall()
    text = "Users:\n"
    for user in result:
        text += f"{user.full_name} | {user.role}\n"
    await message.answer(text)
    


@router.message(F.text == "Content")
async def show_content(message: Message, session):
    content = await session.execute("SELECT id, title FROM content")
    result = content.fetchall()
    text = "Content:\n"
    for item in result:
        text += f"{item.id} | {item.title}\n"
    await message.answer(text)



