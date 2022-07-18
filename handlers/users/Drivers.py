from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.default import tel_button, LineMarkup, Car_needMarkup
from keyboards.default.markup import DriverMarkup
from keyboards.inline import mainMenu1, JAhamarkup, oil_car
from loader import dp, db, bot
from states import RDriver, Cars_Petrol, Cars_Gas, RWay_home, Tex_problem, Reg_petrol


class Drivers:
    def __init__(self, id: int, FIO: str, seria_number_passport: str, phone_number: str):
        self.user_id = id
        self.FIO = FIO
        self.ser_num_passport = seria_number_passport
        self.phone_number = phone_number


class Car_petrol:
    def __init__(self, seria_number_prava: str, mark_avto: str, number_avto: str, seria_numb_texpas: str,
                 km_consumption: float, user_id: int):
        self.ser_num_prava = seria_number_prava
        self.mark_avto = mark_avto
        self.number_avto = number_avto
        self.ser_num_texpas = seria_numb_texpas
        self.km_consumption = km_consumption
        self.user_id = user_id


class Car_gas:
    def __init__(self, seria_number_prava: str, mark_avto: str, number_avto: str, seria_numb_texpas: str,
                 km_consumption: float, user_id: int):
        self.ser_num_prava = seria_number_prava
        self.mark_avto = mark_avto
        self.number_avto = number_avto
        self.ser_num_texpas = seria_numb_texpas
        self.km_consumption = km_consumption
        self.user_id = user_id


class users_loc:
    def __init__(self, last_name: str, user_id: int):
        self.last_name = last_name
        self.user_id = user_id


class tex_problem:
    def __init__(self, user_id: int, tex_problem: str, description: str):
        self.user_id = user_id
        self.tex_problem = tex_problem
        self.description = description


class FUEL:
    def __init__(self, user_id: int, fuel: str, fuel_name: str):
        self.user_id = user_id
        self.fuel = fuel
        self.fuel_name = fuel_name


class Order_day:
    def __init__(self, id: int, user_id: int, date_day: datetime, count_day: float, oil_view: str, view_road: str,
                 oil_day):
        self.id = id
        self.user_id = user_id
        self.date_day = date_day
        self.count_day = count_day
        self.oil_view = oil_view
        self.view_road = view_road
        self.oil_day = oil_day


def get_orders():
    orders = db.select_day()
    users_array = []

    for order in orders:
        users_array.append(Order_day(order[0], order[1], order[2], order[3], order[4], order[5], order[6]))
    return users_array


def get_problems():
    problems = db.select_problem()
    users_array = []

    for problem in problems:
        users_array.append(tex_problem(problem[0], problem[1], problem[2]))
    return users_array


def get_FUEL():
    users = db.select_fuel()
    users_array = []

    for user in users:
        users_array.append(FUEL(user[0], user[1], user[2]))
    return users_array


def get_drivers():
    users = db.get_drivers_admin()
    users_array = []

    for user in users:
        users_array.append(Drivers(user[0], user[1], user[2], user[3]))
    return users_array


def get_gas():
    oil_view = "gas"
    cars = db.get_cars_petrol_admin(oil_view)
    users_array = []
    for car in cars:
        users_array.append(Car_gas(car[0], car[1], car[2], car[3], car[4], car[5]))
    return users_array


def get_petrol():
    oil_view = "petrol"
    cars = db.get_cars_petrol_admin(oil_view)
    users_array = []
    for car in cars:
        users_array.append(Car_petrol(car[0], car[1], car[2], car[3], car[4], car[5]))
    return users_array


def get_chilanzar():
    home = "chilanzar"
    users_id = db.select_users(home)
    users_array = []
    for user in users_id:
        users_array.append(users_loc(user[0], user[1]))
    return users_array


def get_yunusobod():
    home = "yunusobod"
    users_id = db.select_users(home)
    users_array = []
    for user in users_id:
        users_array.append(users_loc(user[0], user[1]))
    return users_array


def get_mirza_ulugbek():
    home = "mirza-ulugbek"
    users_id = db.select_users(home)
    users_array = []
    for user in users_id:
        users_array.append(users_loc(user[0], user[1]))
    return users_array


def get_keles():
    home = "keles"
    users_id = db.select_users(home)
    users_array = []
    for user in users_id:
        users_array.append(users_loc(user[0], user[1]))
    return users_array


@dp.message_handler(Command('driver'))
async def reg_driver(message: types.Message):
    carss = db.select_all_cars_id()
    cars = [driver[0] for driver in carss]
    db.create_table_drivers()
    drivers = db.select_all_drivers_id()
    drivers = [driver[0] for driver in drivers]
    user_id = message.from_user.id
    isregisted1 = db.select_isregis_drivers(user_id)

    regis = "not registered"
    isregisted = db.select_isregis_cars(user_id)

    if user_id in drivers:
        if regis == isregisted1[0][0]:
            await message.answer(
                "Вы не регистрированы.Введите Ф.И.О. ", reply_markup=ReplyKeyboardRemove()
            )
            await RDriver.D1.set()
        elif isregisted1[0][0] == "registered":
            await message.answer(f"Вы уже регистрированы ", reply_markup=DriverMarkup)
    if user_id in cars:
        if regis == isregisted[0][0]:
            await message.answer("Вы не регистрировали машину,выберите топлива : ", reply_markup=mainMenu1, reply=True)

    else:
        await message.answer("Ваша id не регистрирована!!!")
        await message.answer(f"Ваша id {message.from_user.id}")


@dp.message_handler(text="Линии🛣")
async def line_driver(message: types.Message):
    await message.answer("Выберите линию", reply_markup=JAhamarkup)


@dp.message_handler(text='🔙', state=RWay_home.RW1)
async def back_line(message: types.Message, state: FSMContext):
    await message.answer('🔙', reply_markup=DriverMarkup)
    await state.reset_state()


@dp.message_handler(text='🔙')
async def back_line1(message: types.Message, state: FSMContext):
    await message.answer('🔙', reply_markup=DriverMarkup)


@dp.message_handler(text='Обслуга машины🚘')
async def back_line(message: types.Message):
    await message.answer('Выберите какие проблемы ', reply_markup=Car_needMarkup)


@dp.message_handler(text='Топлива')
async def Fuel(message: types.Message):
    await message.answer("Выберите какой выд топлива", reply_markup=oil_car)
    await Reg_petrol.PR1.set()


@dp.callback_query_handler(text_contains="GAS", state=Reg_petrol.PR1)
async def reg_fuel_GAS(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Введите сколько осталось топлива л/m³')
    await Reg_petrol.PR3.set()


@dp.callback_query_handler(text_contains="PETROL", state=Reg_petrol.PR1)
async def reg_fuel_petrol(call: CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer('Введите сколько осталось топлива л/m³')
    await Reg_petrol.PR2.set()


@dp.message_handler(state=Reg_petrol.PR2)
async def reg_fuel_p(message: types.Message, state: FSMContext):
    answer = message.text
    fuel_name = "PETROL"
    user_id = message.from_user.id
    db.add_Feul(user_id, answer, fuel_name)
    await message.answer("Успешно добавлена ! ")
    await state.reset_state()


@dp.message_handler(state=Reg_petrol.PR3)
async def reg_fuel_g(message: types.Message, state: FSMContext):
    answer = message.text
    fuel_name = "GAS"
    user_id = message.from_user.id
    db.add_Feul(user_id, answer, fuel_name)
    await message.answer("Успешно добавлена ! ")
    await state.reset_state()


@dp.message_handler(text='⚙️Тех.Проблемы')
async def tex_PROBLEM(message: types.Message):
    await message.answer('Какие проблемы ?\n Что за проблема ? ')
    await Tex_problem.TP1.set()


@dp.message_handler(state=Tex_problem.TP1)
async def reg1_problem(message: types.Message, state: FSMContext):
    asnwer = message.text
    await state.update_data(problame_name=asnwer)
    await message.answer("Введите описание проблемы : ")
    await Tex_problem.TP2.set()


@dp.message_handler(state=Tex_problem.TP2)
async def reg2_problem(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    user_id = message.from_user.id
    problame_name = data.get("problame_name")
    db.create_table_tex()
    db.add_problem(user_id, problame_name, description)
    await state.reset_state()
    await message.answer("Успешно добавлена !")


@dp.message_handler(state=RDriver.D1)
async def FIO_get(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(FIO=answer)

    await message.answer("Введите номер и серию Паспорта : ")

    await RDriver.next()


@dp.message_handler(state=RDriver.D2)
async def ser_num_passport_get(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(ser_num_passport=answer)
    await message.answer("Отправьте локацию дома")
    await RDriver.D3.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=RDriver.D3)
async def home_location_driver(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    await state.update_data(lat=latitude)
    await state.update_data(long=longitude)
    await message.answer("Отправьте тел.номера, нажав на кнопку ниже!", reply_markup=tel_button.keyboard)

    await RDriver.D4.set()


@dp.message_handler(state=RDriver.D4, content_types=types.ContentType.CONTACT)
async def phone_number(message: types.Message, state: FSMContext):
    data = await state.get_data()
    contact = message.contact
    FIO = data.get("FIO")
    ser_num_passport = data.get("ser_num_passport")
    lat = data.get("lat")
    lat1 = float(lat)
    long = data.get("long")
    long1 = float(long)
    phone_number1 = contact.phone_number
    isregistered = "registered"
    user_id = message.from_user.id
    db.create_table_drivers()
    db.add_drivers(FIO, ser_num_passport, isregistered, phone_number1, lat1, long1, user_id)
    await state.reset_state()
    await message.answer("Вы успешно зарегистрированы", reply_markup=ReplyKeyboardRemove())
    await message.answer(f"Вы уже регистрированы ", reply_markup=DriverMarkup)


@dp.message_handler(Command('car'))
async def reg_car(message: types.Message):
    carss = db.select_all_cars_id()
    cars = [driver[0] for driver in carss]
    user_id = message.from_user.id
    regis = "not registered"
    isregisted = db.select_isregis_cars(user_id)

    if user_id in cars:
        if regis == isregisted[0]:
            await message.answer(
                "Вы не регистрированы,выберите топлива : ", reply_markup=mainMenu1, reply=True
            )

        elif isregisted[0] == "registered":
            await message.answer(f"Вы уже регистрованы ", reply_markup=LineMarkup)

    else:
        await message.answer("Ваша id не регистрирована!!!")
        await message.answer(f"Ваша id {message.from_user.id}")


@dp.callback_query_handler(text_contains="Petrol")
async def Petrol(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Введите серия и номер водительских удостоверения ")
    await Cars_Petrol.Cp1.set()


@dp.callback_query_handler(text_contains="gas")
async def gas(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await call.message.answer("Введите серия и номер водительских удостоверения ")
    await Cars_Gas.Cg1.set()


@dp.message_handler(state=Cars_Petrol.Cp1)
async def prava_ser_num(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(prava_ser_num=answer)
    await message.answer("Введите серия и номер тех.паспорта : ")
    await Cars_Petrol.Cp2.set()


@dp.message_handler(state=Cars_Petrol.Cp2)
async def tex_passport(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(tex_passport=answer)
    await message.answer("Введите марку автомобиля : ")
    await Cars_Petrol.Cp3.set()


@dp.message_handler(state=Cars_Petrol.Cp3)
async def mark_auto(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(mark_avto=answer)
    await message.answer("Введите номер машины : ")
    await Cars_Petrol.Cp4.set()


@dp.message_handler(state=Cars_Petrol.Cp4)
async def car_petrol(message: types.Message, state: FSMContext):
    num_car = message.text
    await state.update_data(num_car=num_car)
    await message.answer("Введите расход машины на 100 км ")
    await Cars_Petrol.next()


@dp.message_handler(state=Cars_Petrol.Cp5)
async def reg_cars(message: types.Message, state: FSMContext):
    km_consumption = float(message.text)
    data = await state.get_data()
    num_car = data.get("num_car")
    tex_passport = data.get("tex_passport")
    oil_view = "petrol"
    mark_avto = data.get("mark_avto")
    prava_ser = data.get("prava_ser_num")
    user_id = message.from_user.id
    isregistered = "registered"
    db.create_table_cars()
    db.add_cars_petrol(prava_ser, mark_avto, tex_passport, num_car, isregistered, km_consumption, oil_view,
                       user_id)
    await message.answer("Вы успешно зарегистрированы", reply_markup=DriverMarkup)
    await state.reset_state()


@dp.message_handler(state=Cars_Gas.Cg1)
async def prava_ser_num_gas(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(prava_ser_num=answer)
    await message.answer("Введите серия и номер тех.паспорта : ")
    await Cars_Gas.Cg2.set()


@dp.message_handler(state=Cars_Gas.Cg2)
async def tex_passport_gas(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(tex_passport=answer)
    await message.answer("Введите марку автомобиля : ")
    await Cars_Gas.Cg3.set()


@dp.message_handler(state=Cars_Gas.Cg3)
async def mark_auto_gas(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(mark_avto=answer)
    await message.answer("Введите номер машины : ")
    await Cars_Gas.Cg4.set()


@dp.message_handler(state=Cars_Gas.Cg4)
async def car_petrol(message: types.Message, state: FSMContext):
    num_car = message.text
    await state.update_data(num_car=num_car)
    await message.answer("Введите расход машины на 100 км ")
    await Cars_Gas.next()


@dp.message_handler(state=Cars_Gas.Cg5)
async def car_gas(message: types.Message, state: FSMContext):
    km_consumption = float(message.text)
    data = await state.get_data()
    tex_passport = data.get("tex_passport")
    mark_avto = data.get("mark_avto")
    oil_view = "gas"
    num_car = data.get("num_car")
    prava_ser = data.get("prava_ser_num")
    user_id = message.from_user.id
    isregistered = "registered"
    db.create_table_cars()
    db.add_cars_gas(prava_ser, mark_avto, tex_passport, num_car, isregistered, km_consumption, oil_view, user_id)
    await message.answer("Вы успешно зарегистрированы", reply_markup=LineMarkup)
    await state.reset_state()
