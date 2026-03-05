from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_panel = ReplyKeyboardMarkup(
    keyboard=[  
        [
            KeyboardButton(text="Управление пользователями"),
            KeyboardButton(text="Управление контентом")
        ],
        [
            KeyboardButton(text="Статистика"),
            KeyboardButton(text="Настройки")
        ],
        [
            KeyboardButton(text="Выйти из админ панели")
        ]
    ],
    resize_keyboard=True
)
