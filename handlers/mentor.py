from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, F

from keyboards.mentor_kb import kb_mentor, kb_role, kb_student, kb_admin
from states.fsm_states import MentorState

router = Router()

mentor_ids = [459976003]
student_ids = [800060636]
admin_ids = [6643230193]


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет сучка!💋", reply_markup=kb_role)


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Тебе нужна помощь?😼", reply_markup=kb_mentor)


@router.callback_query(F.data == "mentor")
async def mentor(callback: CallbackQuery):
    await callback.answer()

    if callback.from_user.id in mentor_ids:
        await callback.message.answer("Вы ментор", reply_markup=kb_mentor)
        await MentorState.name.set()
    else:
        await callback.message.answer("Вы не ментор!\n\n\nДура используй свою роль🖕")


@router.message(MentorState.name)
async def get_name(message: Message):
    name = message.text
    await message.answer(f"Ваше имя: {name}")


@router.callback_query(F.data == "student")
async def student(callback: CallbackQuery):
    await callback.answer()

    if callback.from_user.id in student_ids:
        await callback.message.answer("Вы студент", reply_markup=kb_student)
    else:
        await callback.message.answer("Вы не студент!\n\n\nДура используй свою роль🖕")


@router.callback_query(F.data == "admin")
async def admin(callback: CallbackQuery):
    await callback.answer()

    if callback.from_user.id in admin_ids:
        await callback.message.answer("Вы админ", reply_markup=kb_admin)
    else:
        await callback.message.answer("Вы не админ!\n\n\nДура используй свою роль🖕")