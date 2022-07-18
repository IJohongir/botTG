from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Command
from aiogram.types import ReplyKeyboardRemove

from loader import dp, db
from states import UReg


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    db.create_table_users()
    users = db.select_all_tg_id()
    users = [user[0] for user in users]
    user_id = message.from_user.id
    regis = "not registered"
    isregisted = db.select_isregis(user_id)
    # await message.answer(f"{isregisted[0]}")

    if user_id in users:
        if regis == isregisted[0]:
            await message.answer(
                "Вы не регистрированы. Введите фамилию", reply_markup=ReplyKeyboardRemove()

            )
            await UReg.U1.set()
        elif isregisted[0] == "registered":
            await message.answer(f"Вы уже регистрованы ")

    else:
        await message.answer("Ваша id не регистрирована!!!")
        await message.answer(f"Ваша id {message.from_user.id}")
