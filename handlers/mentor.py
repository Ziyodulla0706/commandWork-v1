from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from keyboards.mentor_kb import kb_mentor, kb_role
from states.fsm_states import MentorState
from database.db_mentor import register_mentor, is_mentor_registered

router = Router()

mentor_ids = [459976003]
student_ids = [800060636]
admin_ids = [6643230193]


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет!💋", reply_markup=kb_role)


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Тебе нужна помощь?😼", reply_markup=kb_mentor)



@router.callback_query(F.data == "mentor")
async def mentor(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.from_user.id in mentor_ids:
        if is_mentor_registered(callback.from_user.id):
            await callback.message.answer("Вы уже зарегистрированы!", reply_markup=kb_mentor)
            return
        await callback.message.answer("Вы ментор! Введите ваше имя:")
        await state.set_state(MentorState.name)
    else:
        await callback.message.answer("Вы не ментор!\n\nИспользуйте свою роль🖕")


@router.message(MentorState.name)
async def get_name(message: Message, state: FSMContext):  
    name = message.text
    register_mentor(message.from_user.id, name, message.from_user.username)
    await message.answer(f"✅ Регистрация завершена!\nВаше имя: {name}", reply_markup=kb_mentor)
    await state.clear() 


@router.callback_query(F.data == "student")
async def student(callback: CallbackQuery):
    await callback.answer()

    if callback.from_user.id in student_ids:
        await callback.message.answer("Вы студент")
    else:
        await callback.message.answer("Вы не студент!\n\nИспользуйте свою роль🖕")


@router.callback_query(F.data == "admin")
async def admin(callback: CallbackQuery):
    await callback.answer()

    if callback.from_user.id in admin_ids:
        await callback.message.answer("Вы админ")
    else:
        await callback.message.answer("Вы не админ!\n\nИспользуйте свою роль🖕")


@router.message(F.text == "👥 Мои студенты")
async def my_students(message: Message):
    await message.answer("Ваши студенты:")

@router.message(F.text == "Статистика")
async def statistics(message: Message):
    await message.answer("Статистика:")

@router.message(F.text == "📝Проверить задания")
async def check_assignments(message: Message):
    await message.answer("Проверить задания:")

