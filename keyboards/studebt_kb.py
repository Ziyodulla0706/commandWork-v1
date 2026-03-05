from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


student_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Просмотр доступных курсов"),
            KeyboardButton(text="Записаться на курс")
        ],
        [
            KeyboardButton(text="Мои курсы"),
            KeyboardButton(text="Посмотреть прогресс")
        ],
        [
            KeyboardButton(text="Сдача домашнего задания")
        ]
    ],
    resize_keyboard=True
)