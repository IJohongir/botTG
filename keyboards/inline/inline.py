from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mainMenu1 = InlineKeyboardMarkup(

    inline_keyboard=[
        [
            InlineKeyboardButton(text="⛽️Бензин", callback_data="Petrol"),
            InlineKeyboardButton(text="🛢ГАЗ", callback_data="gas")

        ]
    ], row_width=2
)
oil_car = InlineKeyboardMarkup(

    inline_keyboard=[
        [
            InlineKeyboardButton(text="⛽️Бензин", callback_data="PETROL"),
            InlineKeyboardButton(text="🛢ГАЗ", callback_data="GAS")

        ]
    ], row_width=2
)
oil_car1 = InlineKeyboardMarkup(

    inline_keyboard=[
        [
            InlineKeyboardButton(text="⛽️Бензин", callback_data="PetroL"),
            InlineKeyboardButton(text="🛢ГАЗ", callback_data="Gas")

        ]
    ], row_width=2
)

YES_NO = InlineKeyboardMarkup(

    inline_keyboard=[
        [
            InlineKeyboardButton(text="ДА", callback_data="YES"),
            InlineKeyboardButton(text="НЕТ", callback_data="NOO")

        ]
    ], row_width=2
)
mainMenu2 = InlineKeyboardMarkup(

    inline_keyboard=[
        [
            InlineKeyboardButton(text="Чиланзар", callback_data="chilanzar"),
            InlineKeyboardButton(text="Юнусабад", callback_data="yunusobod")
        ],
        [
            InlineKeyboardButton(text="Мирза-Улугбек", callback_data="mirza-ulugbek"),
            InlineKeyboardButton(text="Келес", callback_data="keles")
        ]
    ], row_width=2
)
JAhamarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Домой🏚", callback_data="home"),
            InlineKeyboardButton(text="На работу🏢", callback_data="work")
        ]
    ], row_width=2
)

