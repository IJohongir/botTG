from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from keyboards.default import tel_button, UserMarkup
from keyboards.inline import mainMenu2, YES_NO
from loader import dp, db, bot
from states import UReg, Home_loc, EDU_loc, Other_loc


class Users:
    def __init__(
            self, id: int, first_name: str, last_name: str, phone_number: str, name_line: str, is_registed: bool
            # others: float
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.name_line = name_line
        self.is_registed = is_registed

        # self.Others = others


def get_users():
    users = db.get_users_admin()
    users_array = []

    for user in users:
        users_array.append(Users(user[0], user[1], user[2], user[3], user[4], user[5]))
    return users_array


@dp.message_handler(Command('regs'))
async def regf(message: types.Message):
    await message.answer("Введите фамилию:")
    await UReg.U1.set()


@dp.message_handler(state=UReg.U1)
async def first_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(first_name=answer)

    await message.answer("Введите Имя : ")

    await UReg.next()


@dp.message_handler(state=UReg.U2)
async def last_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(last_name=answer)
    await message.answer("Выберите Линию ", reply_markup=mainMenu2)
    await UReg.U3.set()


@dp.callback_query_handler(text_contains="chilanzar", state=UReg.U3)
async def name_line_1(call: CallbackQuery, state: FSMContext):
    await state.update_data(name_line="chilanzar")
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Отправьте тел.номера, нажав на кнопку ниже!", reply_markup=tel_button.keyboard)
    await UReg.U4.set()


@dp.callback_query_handler(text_contains="yunusobod", state=UReg.U3)
async def name_line_2(call: CallbackQuery, state: FSMContext):
    await state.update_data(name_line="yunusobod")
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Отправьте тел.номера, нажав на кнопку ниже!", reply_markup=tel_button.keyboard)
    await UReg.U4.set()


@dp.callback_query_handler(text_contains="mirza-ulugbek", state=UReg.U3)
async def name_line_3(call: CallbackQuery, state: FSMContext):
    await state.update_data(name_line="mirza-ulugbek")
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Отправьте тел.номера, нажав на кнопку ниже!", reply_markup=tel_button.keyboard)
    await UReg.U4.set()


@dp.callback_query_handler(text_contains="keles", state=UReg.U3)
async def name_line_4(call: CallbackQuery, state: FSMContext):
    await state.update_data(name_line="keles")
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Отправьте тел.номера, нажав на кнопку ниже!", reply_markup=tel_button.keyboard)
    await UReg.U4.set()


@dp.message_handler(state=UReg.U4, content_types=types.ContentType.CONTACT)
async def phone_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    contact = message.contact
    first_name1 = data.get("first_name")
    last_name1 = data.get("last_name")
    name_line = data.get("name_line")
    phone_number1 = contact.phone_number
    isregistered = "registered"
    user_id = message.from_user.id
    db.create_table_users()
    db.add_user(first_name1, last_name1, phone_number1, name_line, isregistered, user_id)
    await message.answer("Вы успешно зарегистрированы", reply_markup=ReplyKeyboardRemove())
    await message.answer("Зарегистеруйте и локацию дома", reply_markup=UserMarkup)
    await state.reset_state()


@dp.message_handler(Command('location'))
async def show_location(message: types.Message):
    users = db.select_all_tg_id()
    users = [user[0] for user in users]
    user_id = message.from_user.id
    regis = "not registered"
    isregisted = db.select_isregis(user_id)

    if user_id in users:
        if regis == isregisted[0]:
            await message.answer(
                "Вы не регистрированы. Введите фамилию"

            )
            await UReg.U1.set()
        elif isregisted[0] == "registered":
            await message.answer(f"Вы уже регистрованы ")
            await message.answer("Выберите локацию", reply_markup=UserMarkup)

    else:
        await message.answer("Ваша id не регистрирована!!!")
        await message.answer(f"Ваша id {message.from_user.id}")


@dp.message_handler(text='Адрес дома🏠')
async def home_address(message: types.Message):
    db.create_table_location()
    user_id = message.from_user.id
    users = db.all_tg_id()
    is_registed = db.select_isregis_location(user_id)
    users = [user[0] for user in users]

    regis = "not registered"

    if user_id in users:
        if regis == is_registed[0]:
            await message.answer("Выберите линую ", reply_markup=mainMenu2)
        elif is_registed[0] == "registered":
            await message.answer("🔽", reply_markup=ReplyKeyboardRemove())
            await message.answer("Вы уже отметили свой дом\n Хотите изменит ? ", reply_markup=YES_NO)
    if not (user_id in users):
        db.add_users_loc(user_id, regis)
        await message.answer("Вы только что за регалис, нажмите ещё на 'Адрес дома🏠'")


@dp.callback_query_handler(text_contains="YES")
async def change_home_loc(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id, )
    await call.message.answer("Выберите линую ", reply_markup=mainMenu2)


@dp.callback_query_handler(text_contains="NOO")
async def no_change(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Нафиг нажали на 'Адрес дома🏠'", reply_markup=UserMarkup)


@dp.callback_query_handler(text_contains="chilanzar")
async def get_loc1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.update_data(line="chilanzar")
    await call.message.answer("Отправьте локацию")
    await Home_loc.H1.set()


@dp.callback_query_handler(text_contains="yunusobod")
async def get_loc2(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.update_data(line="yunusobod")
    await call.message.answer("Отправьте локацию")
    await Home_loc.H1.set()


@dp.callback_query_handler(text_contains="mirza-ulugbek")
async def get_loc3(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.update_data(line="mirza-ulugbek")
    await call.message.answer("Отправьте локацию")
    await Home_loc.H1.set()


@dp.callback_query_handler(text_contains="keles")
async def get_loc(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await state.update_data(line="keles")
    await call.message.answer("Отправьте локацию")
    await Home_loc.H1.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=Home_loc.H1)
async def home_location(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    data = await state.get_data()
    name_line = data.get("line")
    is_registed = "registered"
    db.add_location_home(latitude, longitude, name_line, is_registed, user_id)
    await message.answer(f"ваша широта :{latitude},\n ваша долгота {longitude}")
    await message.answer("Успешно добавлено")
    await state.reset_state()


@dp.message_handler(text='Адрес учёбы🏢')
async def EDU_address(message: types.Message):
    user_id = message.from_user.id
    isregisted = db.select_isregis_location(user_id)
    regis = "not registered"
    if isregisted[0] == "registered":
        db.create_table_location()
        await message.answer("Отправьте название учёбы: ")
        await EDU_loc.ED1.set()
    elif isregisted[0] == regis:
        await message.answer("вы не регали Адрес дома🏠 ")
    else:
        await message.answer("Вас нету в базе")


@dp.message_handler(state=EDU_loc.ED1)
async def name_edu(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name_edu=answer)
    await message.answer("Отправьте локацию Учёбы")
    await EDU_loc.ED2.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=EDU_loc.ED2)
async def EDU_location(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    user_id = message.from_user.id
    data = await state.get_data()
    name_edu1 = data.get("name_edu")
    db.add_location_edu(latitude, longitude, name_edu1, user_id)
    await message.answer("Успешно добавлено")
    await state.reset_state()


@dp.message_handler(text='Другие')
async def other_address(message: types.Message):
    user_id = message.from_user.id
    isregisted = db.select_isregis_location(user_id)
    regis = "not registered"
    if isregisted[0] == "registered":
        db.create_table_location()
        await message.answer("Отправьте название Другие места: ")
        await Other_loc.O1.set()
    elif isregisted[0] == regis:
        await message.answer("вы не регали Адрес дома🏠 ")
    else:
        await message.answer("Вас нету в базе")


@dp.message_handler(state=Other_loc.O1)
async def name_other(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name_other=answer)
    await message.answer("Отправьте локацию Другие места")
    await Other_loc.O2.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=Other_loc.O2)
async def Other_location(message: types.Message, state: FSMContext):
    db.create_table_location()
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    data = await state.get_data()
    name_other1 = data.get("name_other")
    user_id = message.from_user.id
    db.other_location(latitude, longitude, name_other1, user_id)
    await state.reset_state()
    await message.answer("Успешно добавлено")
