from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove

from keyboards.default import DriverMarkup
from keyboards.default.markup import DriverMarkup1, Stop_Next
from loader import dp, db, bot
from states import Line_edu, Line_OTHER
from utils.misc.call_distance import choose_shortest


class education_loc:
    def __init__(self, edu_name: str, user_id: int):
        self.edu_name = edu_name
        self.user_id = user_id


class others_loc:
    def __init__(self, other_name: str, user_id: int):
        self.other_name = other_name
        self.user_id = user_id


def get_education():
    edu_name = db.select_edu()
    users_array = []
    for user in edu_name:
        users_array.append(education_loc(user[0], user[1]))
    return users_array


def get_others():
    others = db.select_other()
    users_array = []
    for user in others:
        users_array.append(others_loc(user[0], user[1]))
    return users_array


@dp.message_handler(text="Other🏢/🚘")
async def latitude_ed(message: types.Message):
    await message.answer("Выберите куда ? ", reply_markup=DriverMarkup1)
    await Line_OTHER.LO1.set()


@dp.message_handler(text='🔙', state=Line_OTHER.LO1)
async def back_line_others(message: types.Message, state: FSMContext):
    await message.answer('🔙', reply_markup=DriverMarkup)
    await state.reset_state()


@dp.message_handler(text="EDU(Учёба)", state=Line_OTHER.LO1)
async def EDU_notifiy(message: types.Message, state: FSMContext):
    users = get_education()
    if len(users) == 0:
        await message.answer("Пока что , в этом направление нет пассажиров")
        await state.reset_state()
    elif len(users) != 0:
        for user in users:
            mainMenu2 = InlineKeyboardMarkup(row_width=1)
            mainMenu2.insert(
                InlineKeyboardButton(text=f"{user.edu_name}", callback_data="EDU-" + str(user.user_id))
            )
            await message.answer(
                f"Выбариты : {user.edu_name}",
                reply_markup=mainMenu2
            )
    await Line_edu.next()


@dp.message_handler(text="Other(Другие места)", state=Line_OTHER.LO1)
async def Other_notifiy(message: types.Message, state: FSMContext):
    users = get_others()
    if len(users) == 0:
        await message.answer("Пока что , в этом направление нет пассажиров")
        await state.reset_state()
    elif len(users) != 0:
        for user in users:
            mainMenu2 = InlineKeyboardMarkup(row_width=1)
            mainMenu2.insert(
                InlineKeyboardButton(text=f"{user.other_name}", callback_data="OTHER-" + str(user.user_id))
            )
            await message.answer(
                f"Выбариты : {user.other_name}",
                reply_markup=mainMenu2
            )

    await Line_OTHER.next()


# USER_other_1
@dp.callback_query_handler(text_contains="OTHER-", state=Line_OTHER.LO2)
async def road_locations_other(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_ чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполнятьсtime,я.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:6] == "OTHER-":
        user_id = call.data.split("-")
        await state.update_data(id_other1=user_id)
        data = await state.get_data()
        user_id1 = (data.get("id_other1"))
        user_id2 = int(user_id1[1])
        user_done = db.select_user(user_id2)
        other_location = db.get_other_location(user_id2)
        await call.message.answer_location(other_location[0][0], other_location[0][1])
        doneMArkup = InlineKeyboardMarkup(row_width=1)
        doneMArkup.insert(
            InlineKeyboardButton(text="☑️", callback_data="odone-" + str(user_id2))
        )

        await call.message.answer(f"Выбрали <b>{user_done[0]} </b>", reply_markup=doneMArkup)
        await Line_OTHER.next()


@dp.callback_query_handler(text_contains="odone-", state=Line_OTHER.LO3)
async def done_call_other(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.

    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:6] == "odone-":
        user = call.data.split("-")
        await state.update_data(id_other1=user)
        data = await state.get_data()
        user_id1 = (data.get("id_other1"))
        driver_id = call.from_user.id
        await state.update_data(driver_id=driver_id)
        user_id2 = int(user_id1[1])
        locations = db.get_other_location(user_id2)
        distances = choose_shortest(locations[0][0], locations[0][1])
        oil_view = db.select_oil_view(driver_id)

        if oil_view[0] == "petrol":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distances[0][1], 2)
            oil_pass = round((km_consumption[0] / 100) * round(distances[0][1], 2), 3)
            await state.update_data(oil_pass1=oil_pass)
            await state.update_data(petrol_count1=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        elif oil_view[0] == "gas":
            km_consumption = db.select_km_consumption(driver_id)
            distan = float(distances[0][1])
            update_count = round(distan, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distan, 2), 3)
            await state.update_data(oil_gas1=oil_pass)
            await state.update_data(gas_count1=update_count)
        else:
            await call.message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
            await state.reset_state()
    await Line_OTHER.next()


@dp.message_handler(text="Stop", state=Line_OTHER.LO4)
async def Stop_user_other(message: types.Message, state: FSMContext):
    data = await state.get_data()
    driver = data.get("driver_id")
    driver_id = int(driver)
    date = message.date
    user_id1 = (data.get("id_other1"))
    user_id2 = int(user_id1[1])
    locations = db.get_locations_home(user_id2)
    distances = choose_shortest(locations[0][0], locations[0][1])
    oil_view = db.select_oil_view(driver_id)

    if oil_view[0] == "petrol":

        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances[0][1], 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances[0][1], 2), 3)
        oil_pa1 = data.get("oil_pass1")
        oil_pass1 = float(oil_pa1)
        update_cou1 = data.get("petrol_count1")
        update_count1 = float(update_cou1)
        sum_count = update_count + update_count1
        sum_oil = oil_pass + oil_pass1
        db.create_table_road_consumption()
        view_road = "Другие места"
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    elif oil_view[0] == "gas":

        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances[0][1], 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances[0][1], 2), 3)
        oil_pa1 = data.get("oil_gas1")
        oil_gass1 = float(oil_pa1)
        update_cou1 = data.get("gas_count1")
        update_count1 = float(update_cou1)
        sum_count = 2 * (update_count + update_count1)
        sum_oil = 2 * (oil_pass + oil_gass1)
        view_road = "Другие места"
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    else:
        await message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
        await state.reset_state()


@dp.callback_query_handler(text_contains="EDU-", state=Line_edu.LE1)
async def road_locations_edu(call: CallbackQuery, state: FSMContext):
    driver = call.from_user.id
    await state.update_data(driver_id=driver)
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_ чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполнятьсtime,я.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:4] == "EDU-":
        user_id = call.data.split("-")
        await state.update_data(id_edu1=user_id)
        data = await state.get_data()
        user_id1 = (data.get("id_edu1"))
        user_id2 = int(user_id1[1])
        user_done = db.select_user(user_id2)
        edu_location = db.get_edu_location(user_id2)
        await call.message.answer_location(edu_location[0][0], edu_location[0][1])
        doneMArkup = InlineKeyboardMarkup(row_width=1)
        doneMArkup.insert(
            InlineKeyboardButton(text="☑️", callback_data="edone-" + str(user_id2))
        )

        await call.message.answer(f"Выбрали <b>{user_done[0]} </b>", reply_markup=doneMArkup)
        await Line_edu.next()


@dp.callback_query_handler(text_contains="edone-", state=Line_edu.LE2)
async def done_call_edu(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.

    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:6] == "edone-":
        data = await state.get_data()
        user_id1 = (data.get("id_edu1"))
        driver = data.get("driver_id")
        driver_id = int(driver)
        user_id2 = int(user_id1[1])
        locations = db.get_edu_location(user_id2)
        distances = choose_shortest(locations[0][0], locations[0][1])
        oil_view = db.select_oil_view(driver_id)

        if oil_view[0] == "petrol":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distances[0][1], 2)
            oil_pass = round((km_consumption[0] / 100) * round(distances[0][1], 2), 3)
            await state.update_data(oil_pass1=oil_pass)
            await state.update_data(petrol_count1=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        elif oil_view[0] == "gas":
            km_consumption = db.select_km_consumption(driver_id)
            distan = float(distances[0][1])
            update_count = round(distan, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distan, 2), 3)
            await state.update_data(oil_gas1=oil_pass)
            await state.update_data(gas_count1=update_count)
        else:
            await call.message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
            await state.reset_state()
    await Line_edu.next()


@dp.message_handler(text="Stop", state=Line_edu.LE3)
async def Stop_user_edu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    driver = data.get("driver_id")
    driver_id = int(driver)
    date = message.date
    user_id1 = (data.get("id_edu1"))
    user_id2 = int(user_id1[1])
    locations = db.get_edu_location(user_id2)
    distances = choose_shortest(locations[0][0], locations[0][1])
    oil_view = db.select_oil_view(driver_id)

    if oil_view[0] == "petrol":

        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances[0][1], 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances[0][1], 2), 3)
        oil_pa1 = data.get("oil_pass1")
        oil_pass1 = float(oil_pa1)
        update_cou1 = data.get("petrol_count1")
        update_count1 = float(update_cou1)
        sum_count = update_count + update_count1
        sum_oil = oil_pass + oil_pass1
        db.create_table_road_consumption()
        view_road = "Учёба"
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    elif oil_view[0] == "gas":

        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances[0][1], 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances[0][1], 2), 3)
        oil_pa1 = data.get("oil_gas1")
        oil_gass1 = float(oil_pa1)
        update_cou1 = data.get("gas_count1")
        update_count1 = float(update_cou1)
        sum_count = update_count + update_count1
        sum_oil = oil_pass + oil_gass1
        view_road = "Учёба"
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    else:
        await message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
        await state.reset_state()
