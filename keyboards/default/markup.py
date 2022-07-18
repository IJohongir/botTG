from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

adminMarkup = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton('🏎Водители'),
            KeyboardButton("🚘Машины🚘"),

        ],
        [
            KeyboardButton('🙍🏻‍♀️/🙎🏽‍♂️Пассажиры'),
            KeyboardButton('Новое(🛣,user,driver,new Admin)'),
            KeyboardButton('Отчеты & Тех.Проблемы')
        ]
    ], resize_keyboard=True
)
newMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('🙍🏻‍♀️/🙎🏽‍♂️User'), KeyboardButton("🏎Car")
        ],
        [
            KeyboardButton('🙍‍♂️Driver'), KeyboardButton('new Admin'), KeyboardButton('◀️Назад')
        ]
    ], resize_keyboard=True
)
SettingMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('🧾Отчет(ВСЕ)'),
            KeyboardButton('⚙️Тех.Проблемы(admin)'),
            KeyboardButton("⛽️Топлива")
        ],
        [
            KeyboardButton('◀️Назад')
        ]
    ], resize_keyboard=True
)
Stop_Next = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Stop"),
            KeyboardButton(text="Next")
        ]
    ], resize_keyboard=True
)

UserMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Адрес дома🏠'),
            KeyboardButton(text='Адрес учёбы🏢'),
            KeyboardButton(text='Другие'),
            KeyboardButton(text='Где я ?📍', request_location=True)

        ]
    ], resize_keyboard=True
)
DriverMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Линии🛣"), KeyboardButton("Other🏢/🚘"),
            KeyboardButton("Обслуга машины🚘")

        ]
    ], resize_keyboard=True
)
DriverMarkup1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("EDU(Учёба)"),
            KeyboardButton("Other(Другие места)"), KeyboardButton('🔙')
        ]
    ], resize_keyboard=True
)
LineMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Чиланзар"),
            KeyboardButton("Юнусабад")

        ],
        [KeyboardButton("Мирза-Улугбек"),
         KeyboardButton("Келес"), KeyboardButton('🔙')
         ]
    ], resize_keyboard=True
)
Car_needMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('⚙️Тех.Проблемы'),
            KeyboardButton("Топлива"),
            KeyboardButton('🔙')
        ]
    ], resize_keyboard=True
)
