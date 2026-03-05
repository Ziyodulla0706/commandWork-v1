from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database.db import SessionLocal
from database.models import Course, Enrollment, Homework, Student  # подставь ваши модели
from states.student_states import SubmitHW

router = Router()

@router.message(F.text == "Просмотр доступных курсов")
async def view_courses(message: Message):
    # Тут НЕ нужно спрашивать название курса — надо показать список
    with SessionLocal() as db:
        courses = db.query(Course).all()

    if not courses:
        await message.answer("Курсов пока нет.")
        return

    text = "📚 Доступные курсы:\n" + "\n".join([f"• {c.name}" for c in courses])
    await message.answer(text)


@router.message(F.text == "Записаться на курс")
async def enroll_start(message: Message, state: FSMContext):
    await message.answer("Введите название курса, на который хотите записаться:")
    await state.set_state(SubmitHW.waiting_course_name)


@router.message(SubmitHW.waiting_course_name)
async def enroll_finish(message: Message, state: FSMContext):
    course_name = message.text.strip()

    with SessionLocal() as db:
        course = db.query(Course).filter(Course.name == course_name).first()
        if not course:
            await message.answer("Курс не найден. Проверь название.")
            return

        # пример: как найти студента по telegram_id (если у вас так хранится)
        student = db.query(Student).filter(Student.telegram_id == message.from_user.id).first()
        if not student:
            await message.answer("Вы не зарегистрированы. Нажмите /start.")
            return

        exists = db.query(Enrollment).filter(
            Enrollment.student_id == student.id,
            Enrollment.course_id == course.id
        ).first()
        if exists:
            await message.answer("Вы уже записаны на этот курс.")
            await state.clear()
            return

        db.add(Enrollment(student_id=student.id, course_id=course.id))
        db.commit()

    await message.answer(f"✅ Вы записались на курс: {course_name}")
    await state.clear()


@router.message(F.text == "Мои курсы")
async def my_courses(message: Message):
    with SessionLocal() as db:
        student = db.query(Student).filter(Student.telegram_id == message.from_user.id).first()
        if not student:
            await message.answer("Вы не зарегистрированы. Нажмите /start.")
            return

        rows = db.query(Course.name).join(Enrollment, Enrollment.course_id == Course.id)\
            .filter(Enrollment.student_id == student.id).all()

    if not rows:
        await message.answer("У вас нет курсов.")
        return

    text = "🎓 Ваши курсы:\n" + "\n".join([f"• {name}" for (name,) in rows])
    await message.answer(text)


@router.message(F.text == "Посмотреть прогресс")
async def view_progress(message: Message):
    # Прогресс обычно считается по Homework.status
    with SessionLocal() as db:
        student = db.query(Student).filter(Student.telegram_id == message.from_user.id).first()
        if not student:
            await message.answer("Вы не зарегистрированы. Нажмите /start.")
            return

        total = db.query(Homework).filter(Homework.student_id == student.id).count()
        approved = db.query(Homework).filter(Homework.student_id == student.id, Homework.status == "approved").count()
        rejected = db.query(Homework).filter(Homework.student_id == student.id, Homework.status == "rejected").count()
        pending = db.query(Homework).filter(Homework.student_id == student.id, Homework.status == "pending").count()

    await message.answer(
        f"📈 Ваш прогресс по ДЗ:\n"
        f"Всего: {total}\n"
        f"✅ Принято: {approved}\n"
        f"❌ Отклонено: {rejected}\n"
        f"⏳ В ожидании: {pending}"
    )


@router.message(F.text == "Сдача домашнего задания")
async def submit_hw_start(message: Message, state: FSMContext):
    await message.answer("Введите название курса для сдачи ДЗ:")
    await state.set_state(SubmitHW.waiting_course_name)


@router.message(SubmitHW.waiting_course_name, F.text)
async def submit_hw_course(message: Message, state: FSMContext):
    await state.update_data(course_name=message.text.strip())
    await message.answer("Отправьте домашнее задание текстом или файлом:")
    await state.set_state(SubmitHW.waiting_content)


@router.message(SubmitHW.waiting_content)
async def submit_hw_content(message: Message, state: FSMContext):
    data = await state.get_data()
    course_name = data["course_name"]

    content = None
    if message.text:
        content = message.text.strip()
    elif message.document:
        content = message.document.file_id

    if not content:
        await message.answer("Пришлите текст или документ-файл.")
        return

    with SessionLocal() as db:
        course = db.query(Course).filter(Course.name == course_name).first()
        if not course:
            await message.answer("Курс не найден.")
            return

        student = db.query(Student).filter(Student.telegram_id == message.from_user.id).first()
        if not student:
            await message.answer("Вы не зарегистрированы. Нажмите /start.")
            return

        db.add(Homework(
            student_id=student.id,
            course_id=course.id,
            content=content,
            status="pending"
        ))
        db.commit()

    await message.answer("✅ ДЗ отправлено на проверку.")
    await state.clear()