from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove

from handlers.users.Drivers import get_chilanzar, get_yunusobod, get_mirza_ulugbek, get_keles
from keyboards.default import LineMarkup
from keyboards.default.markup import Stop_Next
from loader import dp, db, bot
from states import RWay_home
from utils.misc.call_distance import choose_shortest, calc_distance


@dp.message_handler(text="Чиланзар", state=RWay_home.RW1)
async def road_chilanzar(message: types.Message, state: FSMContext):
    users = get_chilanzar()
    if len(users) == 0:
        await message.answer("Пока что , в этом направление нет пассажиров")
        await state.reset_state()
    elif len(users) != 0:
        for user in users:
            mainMenu2 = InlineKeyboardMarkup(row_width=1)
            mainMenu2.insert(
                InlineKeyboardButton(text=f"{user.last_name}", callback_data="User-" + str(user.user_id))
            )
            await message.answer(
                f"Выбариты : {user.last_name}",
                reply_markup=mainMenu2
            )
        await RWay_home.next()


@dp.message_handler(text="Юнусабад", state=RWay_home.RW1)
async def road_yunusobod(message: types.Message):
    users = get_yunusobod()
    if len(users) == 0:
        await message.answer("Пока что , в этом направление нет пассажиров")
        await RWay_home.RW1.set()
    elif len(users) != 0:
        for user in users:
            mainMenu2 = InlineKeyboardMarkup(row_width=1)
            mainMenu2.insert(
                InlineKeyboardButton(text=f"{user.last_name}", callback_data="User-" + str(user.user_id))
            )
            await message.answer(
                f"Выбариты : {user.last_name}",
                reply_markup=mainMenu2
            )

        await RWay_home.next()


@dp.message_handler(text="Мирза-Улугбек", state=RWay_home.RW1)
async def road_mirza_ulugbek(message: types.Message):
    users = get_mirza_ulugbek()
    if len(users) == 0:
        await message.answer("Пока что , в этом направление нет пассажиров")
        await RWay_home.RW1.set()
    elif len(users) != 0:
        for user in users:
            mainMenu2 = InlineKeyboardMarkup(row_width=1)
            mainMenu2.insert(
                InlineKeyboardButton(text=f"{user.last_name}", callback_data="User-" + str(user.user_id))
            )
            await message.answer(
                f"Выбариты : {user.last_name}",
                reply_markup=mainMenu2
            )
        await RWay_home.next()


@dp.message_handler(text="Келес", state=RWay_home.RW1)
async def road_keles(message: types.Message):
    users = get_keles()
    if len(users) == 0:
        await message.answer("Пока что , в этом направление нет пассажиров")
        await RWay_home.RW1.set()
    elif len(users) != 0:
        for user in users:
            mainMenu2 = InlineKeyboardMarkup(row_width=1)
            mainMenu2.insert(
                InlineKeyboardButton(text=f"{user.last_name}", callback_data="User-" + str(user.user_id))
            )
            await message.answer(
                f"Выбариты : {user.last_name}",
                reply_markup=mainMenu2
            )
        await RWay_home.next()


@dp.callback_query_handler(text_contains="home")
async def road_notify_home(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await state.update_data(driver_id=user_id)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Выберите линию", reply_markup=LineMarkup)
    await RWay_home.RW1.set()


# USER1#

@dp.callback_query_handler(text_contains="User-", state=RWay_home.RW2)
async def road_locations_home(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:5] == "User-":
        user_id = call.data.split("-")
        await state.update_data(id_Sprint=user_id)
        data = await state.get_data()
        user_id1 = (data.get("id_Sprint"))
        user_id2 = int(user_id1[1])
        locations = db.get_locations_home(user_id2)
        user_done = db.select_user(user_id2)
        await state.update_data(name_user=user_done[0])
        await call.message.answer_location(locations[0][0], locations[0][1])
        doneMArkup = InlineKeyboardMarkup(row_width=1)
        doneMArkup.insert(
            InlineKeyboardButton(text="☑️", callback_data="done-" + str(user_id2))
        )

        await call.message.answer(f"Выбрали <b>{user_done[0]} </b>", reply_markup=doneMArkup)
        await RWay_home.next()


@dp.callback_query_handler(text_contains="done-", state=RWay_home.RW3)
async def done_call_home(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.

    await call.answer(cache_time=100)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:5] == "done-":
        user = call.data.split("-")
        await state.update_data(id_Sprint=user)
        data = await state.get_data()
        user_id1 = (data.get("id_Sprint"))
        driver = data.get("driver_id")
        driver_id = int(driver)
        user_id2 = int(user_id1[1])
        locations = db.get_locations_home(user_id2)
        distances = choose_shortest(locations[0][0], locations[0][1])
        await state.update_data(work_distance=distances)
        distan = float(distances[0][1])
        oil_view = db.select_oil_view(driver_id)
        # text = "\n\n".join([f"Кто это: {user_name}.\n Расстояние до него: {distance:.1f} км."

        if oil_view[0] == "petrol":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distan, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distan, 2), 3)
            await state.update_data(oil_pass1=oil_pass)
            await state.update_data(petrol_count1=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        elif oil_view[0] == "gas":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distan, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distan, 2), 3)
            await state.update_data(oil_gas1=oil_pass)
            await state.update_data(gas_count1=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        else:
            await call.message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
            await state.reset_state()

    await call.message.answer("Если поездка окончена нажмите на 'Stop' или 'Next' что бы продолжить ")
    await RWay_home.next()


@dp.message_handler(text='Next', state=RWay_home.RW4)
async def Next_user1(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message_id)
    await message.answer("Поездка продолжается", reply_markup=ReplyKeyboardRemove())
    await RWay_home.RW4.set()


@dp.message_handler(text="Stop", state=RWay_home.RW4)
async def Stop_user1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    driver = data.get("driver_id")
    driver_id = int(driver)
    date = message.date
    user_id1 = (data.get("id_Sprint"))
    user_id2 = int(user_id1[1])
    locations = db.get_locations_home(user_id2)
    driver_locations = db.get_home_driver(driver_id)
    distances = calc_distance(locations[0][0], locations[0][1], driver_locations[0][0], driver_locations[0][1])
    oil_view = db.select_oil_view(driver_id)

    if oil_view[0] == "petrol":
        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances, 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
        oil_pa1 = data.get("oil_pass1")
        oil_pass1 = float(oil_pa1)
        update_cou1 = data.get("petrol_count1")
        update_count1 = float(update_cou1)
        sum_count = update_count + update_count1
        sum_oil = oil_pass + oil_pass1
        view_road = "Домой"
        db.create_table_road_consumption()
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    elif oil_view[0] == "gas":
        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances, 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
        oil_pa1 = data.get("oil_gas1")
        oil_gass1 = float(oil_pa1)
        update_cou1 = data.get("gas_count1")
        update_count1 = float(update_cou1)
        sum_count = update_count + update_count1
        view_road = "Домой"
        sum_oil = oil_pass + oil_gass1
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    else:
        await message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
        await state.reset_state()


# USER1 END

# USER2#
@dp.callback_query_handler(text_contains="User-", state=RWay_home.RW4)
async def road_locations1_home(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:5] == "User-":
        user_id = call.data.split("-")
        await state.update_data(id_Sprint1=user_id)
        data = await state.get_data()
        user_id1 = data.get("id_Sprint1")
        user_id2 = int(user_id1[1])
        locations = db.get_locations_home(user_id2)
        user_done = db.select_user(user_id2)
        await state.update_data(name_user=user_done[0])
        await call.message.answer_location(locations[0][0], locations[0][1])
        doneMArkup = InlineKeyboardMarkup(row_width=1)
        doneMArkup.insert(
            InlineKeyboardButton(text="☑️", callback_data="done-" + str(user_id2))
        )

        await call.message.answer(f"Выбрали <b>{user_done[0]} </b>", reply_markup=doneMArkup)
        await RWay_home.next()


@dp.callback_query_handler(text_contains="done-", state=RWay_home.RW5)
async def done_call1_home(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=25)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:5] == "done-":
        user = call.data.split("-")
        await state.update_data(id_Sprint1=user)
        data = await state.get_data()
        user_i2 = data.get("id_Sprint1")
        user_id1 = (data.get("id_Sprint"))
        driver = data.get("driver_id")
        driver_id = int(driver)
        user2 = int(user_i2[1])
        user_id2 = int(user_id1[1])
        locations = db.get_locations_home(user_id2)
        locations1 = db.get_locations_home(user2)
        distances = calc_distance(locations[0][0], locations[0][1], locations1[0][0], locations1[0][1])
        await call.message.answer(f"Distance  {distances:.2f} km")
        oil_view = db.select_oil_view(driver_id)

        if oil_view[0] == "petrol":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distances, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
            await state.update_data(oil_pass2=oil_pass)
            await state.update_data(petrol_count2=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        elif oil_view[0] == "gas":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distances, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
            await state.update_data(oil_gas2=oil_pass)
            await state.update_data(gas_count2=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        else:
            await call.message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
            await state.reset_state()

        await call.message.answer("Если поездка окончена нажмите на 'Stop' или 'Next' что бы продолжить ")
        await RWay_home.next()


@dp.message_handler(text='Next', state=RWay_home.RW6)
async def Next_user2_home(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    await message.answer("Поездка продолжается", reply_markup=ReplyKeyboardRemove())
    await RWay_home.RW6.set()


@dp.message_handler(text="Stop", state=RWay_home.RW6)
async def Stop_user2_home(message: types.Message, state: FSMContext):
    data = await state.get_data()
    driver = data.get("driver_id")
    driver_id = int(driver)
    date = message.date
    user_id1 = (data.get("id_Sprint1"))
    user_id2 = int(user_id1[1])
    locations = db.get_locations_home(user_id2)
    driver_locations = db.get_home_driver(driver_id)
    distances = calc_distance(locations[0][0], locations[0][1], driver_locations[0][0], driver_locations[0][1])
    oil_view = db.select_oil_view(driver_id)

    if oil_view[0] == "petrol":
        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances, 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
        oil_pa1 = data.get("oil_pass1")
        oil_pass1 = float(oil_pa1)
        update_cou1 = data.get("petrol_count1")
        update_count1 = float(update_cou1)
        oil_pa2 = data.get("oil_pass2")
        oil_pass2 = float(oil_pa2)
        update_cou2 = data.get("petrol_count2")
        update_count2 = float(update_cou2)
        sum_count = update_count + update_count1 + update_count2
        sum_oil = oil_pass + oil_pass1 + oil_pass2
        view_road = "Домой"
        db.create_table_road_consumption()
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    elif oil_view[0] == "gas":
        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances, 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
        oil_pa1 = data.get("oil_gas1")
        oil_gass1 = float(oil_pa1)
        update_cou1 = data.get("gas_count1")
        update_count1 = float(update_cou1)
        oil_pa2 = data.get("oil_gas2")
        oil_gass2 = float(oil_pa2)
        update_cou2 = data.get("gas_count2")
        update_count2 = float(update_cou2)
        sum_count = update_count + update_count1 + update_count2
        sum_oil = oil_pass + oil_gass1 + oil_gass2
        view_road = "Домой"
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    else:
        await message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
        await state.reset_state()


# USER2 END#

# USER3 #
@dp.callback_query_handler(text_contains="User-", state=RWay_home.RW6)
async def road_locations2_home(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:5] == "User-":
        user_id = call.data.split("-")
        await state.update_data(id_Sprint2=user_id)
        data = await state.get_data()
        user_id1 = data.get("id_Sprint2")
        user_id2 = int(user_id1[1])
        locations = db.get_locations_home(user_id2)
        user_done = db.select_user(user_id2)
        await state.update_data(name_user=user_done[0])
        await call.message.answer_location(locations[0][0], locations[0][1])
        doneMArkup = InlineKeyboardMarkup(row_width=1)
        doneMArkup.insert(
            InlineKeyboardButton(text="☑️", callback_data="done-" + str(user_id2))
        )

        await call.message.answer(f"Выбрали <b>{user_done[0]} </b>", reply_markup=doneMArkup)
        await RWay_home.next()


@dp.callback_query_handler(text_contains="done-", state=RWay_home.RW7)
async def done_call2_home(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=25)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:5] == "done-":
        user = call.data.split("-")
        await state.update_data(id_Sprint2=user)
        data = await state.get_data()
        user_i2 = data.get("id_Sprint2")
        user_id1 = (data.get("id_Sprint1"))
        user2 = int(user_i2[1])
        user_id2 = int(user_id1[1])
        driver = data.get("driver_id")
        driver_id = int(driver)
        locations = db.get_locations_home(user_id2)
        locations1 = db.get_locations_home(user2)
        distances = calc_distance(locations[0][0], locations[0][1], locations1[0][0], locations1[0][1])
        oil_view = db.select_oil_view(driver_id)

        if oil_view[0] == "petrol":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distances, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
            await state.update_data(oil_pass3=oil_pass)
            await state.update_data(petrol_count3=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        elif oil_view[0] == "gas":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distances, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
            await state.update_data(oil_gas3=oil_pass)
            await state.update_data(gas_count3=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        else:
            await call.message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
            await state.reset_state()

    await call.message.answer("Если поездка окончена нажмите на 'Stop' или 'Next' что бы продолжить ")
    await RWay_home.next()


@dp.message_handler(text="Stop", state=RWay_home.RW8)
async def Stop_driver3_home(message: types.Message, state: FSMContext):
    data = await state.get_data()
    driver = data.get("driver_id")
    driver_id = int(driver)
    date = message.date
    user_id1 = (data.get("id_Sprint2"))
    user_id2 = int(user_id1[1])
    locations = db.get_locations_home(user_id2)
    driver_locations = db.get_home_driver(driver_id)
    distances = calc_distance(locations[0][0], locations[0][1], driver_locations[0][0], driver_locations[0][1])
    oil_view = db.select_oil_view(driver_id)

    if oil_view[0] == "petrol":
        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances, 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
        oil_pa1 = data.get("oil_pass1")
        oil_pass1 = float(oil_pa1)
        update_cou1 = data.get("petrol_count1")
        update_count1 = float(update_cou1)
        oil_pa2 = data.get("oil_pass2")
        oil_pass2 = float(oil_pa2)
        update_cou2 = data.get("petrol_count2")
        update_count2 = float(update_cou2)
        oil_pa3 = data.get("oil_pass3")
        oil_pass3 = float(oil_pa3)
        update_cou3 = data.get("petrol_count3")
        update_count3 = float(update_cou3)
        view_road = "Домой"
        sum_count = update_count + update_count1 + update_count2 + update_count3
        sum_oil = oil_pass + oil_pass1 + oil_pass2 + oil_pass3
        db.create_table_road_consumption()
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    elif oil_view[0] == "gas":
        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distances, 2)
        oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
        oil_pa1 = data.get("oil_gas1")
        view_road = "Домой"
        oil_gass1 = float(oil_pa1)
        update_cou1 = data.get("gas_count1")
        update_count1 = float(update_cou1)
        oil_pa2 = data.get("oil_gas2")
        oil_gass2 = float(oil_pa2)
        update_cou2 = data.get("gas_count2")
        update_count2 = float(update_cou2)
        oil_pa3 = data.get("oil_gas3")
        oil_gass3 = float(oil_pa3)
        update_cou3 = data.get("gas_count3")
        update_count3 = float(update_cou3)
        sum_count = update_count + update_count1 + update_count2 + update_count3
        sum_oil = oil_pass + oil_gass1 + oil_gass2 + oil_gass3
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    else:
        await message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
        await state.reset_state()


# USER3 END#

# USER4 #
@dp.callback_query_handler(text_contains="User-", state=RWay_home.RW9)
async def road_locations2_home(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:5] == "User-":
        user_id = call.data.split("-")
        await state.update_data(id_Sprint3=user_id)
        data = await state.get_data()
        user_id1 = data.get("id_Sprint3")
        user_id2 = int(user_id1[1])
        locations = db.get_locations_home(user_id2)
        user_done = db.select_user(user_id2)
        await state.update_data(name_user=user_done[0])
        await call.message.answer_location(locations[0][0], locations[0][1])
        doneMArkup = InlineKeyboardMarkup(row_width=1)
        doneMArkup.insert(
            InlineKeyboardButton(text="☑️", callback_data="done-" + str(user_id2))
        )

        await call.message.answer(f"Выбрали <b>{user_done[0]} </b>", reply_markup=doneMArkup)
        await RWay_home.next()


@dp.callback_query_handler(text_contains="done-", state=RWay_home.RW10)
async def done_call2_home(call: CallbackQuery, state: FSMContext):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=25)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if call.data[0:5] == "done-":
        user = call.data.split("-")
        await state.update_data(id_Sprint3=user)
        data = await state.get_data()
        user_i2 = data.get("id_Sprint3")
        user_id1 = (data.get("id_Sprint2"))
        driver = data.get("driver_id")
        driver_id = int(driver)
        user2 = int(user_i2[1])
        user_id2 = int(user_id1[1])
        locations = db.get_locations_home(user_id2)
        locations1 = db.get_locations_home(user2)
        distances = calc_distance(locations[0][0], locations[0][1], locations1[0][0], locations1[0][1])
        oil_view = db.select_oil_view(driver_id)

        if oil_view[0] == "petrol":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distances, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
            await state.update_data(oil_pass4=oil_pass)
            await state.update_data(petrol_count4=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        elif oil_view[0] == "gas":
            km_consumption = db.select_km_consumption(driver_id)
            update_count = round(distances, 2)
            oil_pass = round((km_consumption[0] / 100) * round(distances, 2), 3)
            await state.update_data(oil_gas4=oil_pass)
            await state.update_data(gas_count4=update_count)
            await call.message.answer("Продолжить поездку ? ", reply_markup=Stop_Next)

        else:
            await call.message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
            await state.reset_state()

    await call.message.answer("Если поездка окончена нажмите на 'Stop' или 'Next' что бы продолжить ")
    await RWay_home.next()


# USERs END
@dp.message_handler(state=RWay_home.RW11)
async def return_way(message: types.Message, state: FSMContext):
    await message.answer("Больше 4-ых нет пассажиров ")
    await message.answer("нажмите на 'Stop' ", reply_markup=Stop_Next)
    await RWay_home.RW8.set()


@dp.message_handler(text="Stop", state=RWay_home.RW11)
async def Stop_user3_work(message: types.Message, state: FSMContext):
    data = await state.get_data()
    driver = data.get("driver_id")
    driver_id = int(driver)
    date = message.date
    user_id1 = (data.get("id_Sprint3"))
    user_id2 = int(user_id1[1])
    locations = db.get_locations_home(user_id2)
    distances = choose_shortest(locations[0][0], locations[0][1])
    distan = float(distances[0][1])
    oil_view = db.select_oil_view(driver_id)

    if oil_view[0] == "petrol":

        km_consumption = db.select_km_consumption(driver_id)
        update_count = round(distan, 2)
        oil_pass = round((km_consumption[0] / 100) * round(distan, 2), 3)
        view_road = "Домой"
        oil_pa1 = data.get("oil_pass1")
        oil_pass1 = float(oil_pa1)
        update_cou1 = data.get("petrol_count1")
        update_count1 = float(update_cou1)
        oil_pa4 = data.get("oil_pass4")
        oil_pass4 = float(oil_pa4)
        update_cou4 = data.get("petrol_count4")
        update_count4 = float(update_cou4)
        oil_pa3 = data.get("oil_pass3")
        oil_pass3 = float(oil_pa3)
        update_cou3 = data.get("petrol_count3")
        update_count3 = float(update_cou3)
        oil_pa2 = data.get("oil_pass2")
        oil_pass2 = float(oil_pa2)
        update_cou2 = data.get("petrol_count2")
        update_count2 = float(update_cou2)
        sum_count = update_count + update_count1 + update_count2 + update_count3 + update_count4
        sum_oil = oil_pass4 + oil_pass3 + oil_pass2 + oil_pass1 + oil_pass
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    elif oil_view[0] == "gas":

        km_consumption = db.select_km_consumption(driver_id)
        distan = float(distances[0][1])
        update_count = round(distan, 2)
        oil_pass = round((km_consumption[0] / 100) * round(distan, 2), 3)
        oil_pa4 = data.get("oil_gas4")
        oil_gass4 = float(oil_pa4)
        update_cou4 = data.get("gas_count4")
        update_count4 = float(update_cou4)
        oil_pa3 = data.get("oil_gas3")
        oil_gass3 = float(oil_pa3)
        view_road = "Домой"
        update_cou3 = data.get("gas_count3")
        update_count3 = float(update_cou3)
        oil_pa2 = data.get("oil_gas2")
        oil_gass2 = float(oil_pa2)
        update_cou2 = data.get("gas_count2")
        update_count2 = float(update_cou2)
        oil_pa1 = data.get("oil_gas1")
        oil_gass1 = float(oil_pa1)
        update_cou1 = data.get("gas_count1")
        update_count1 = float(update_cou1)
        sum_count = update_count + update_count1 + update_count2 + update_count3 + update_count4
        sum_oil = oil_pass + oil_gass1 + oil_gass2 + oil_gass3 + oil_gass4
        db.insert_day(date, sum_count, sum_oil, oil_view[0], view_road, driver_id)
        await message.answer("Поездка окончено", reply_markup=ReplyKeyboardRemove())
        await state.reset_state()

    else:
        await message.answer("Вас нету в базе!!!!!!!!!!!!!!!")
        await state.reset_state()
# USER4 END
