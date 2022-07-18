from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("admin", "Для администратора"),
        types.BotCommand("driver", "Для водителя"),
        types.BotCommand("location", "Для добавлении локации"),
        types.BotCommand("car", "регистрация машин")

    ])
