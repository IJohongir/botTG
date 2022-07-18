import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, CallbackQuery

from data.config import admins
from handlers.users.Drivers import get_drivers, get_gas, get_petrol, get_problems, get_FUEL, get_orders
from handlers.users.Users import get_users
from keyboards.default import adminMarkup, newMarkup, SettingMarkup
from keyboards.inline import oil_car1
from loader import dp, db, bot
from states import Id_driver, New_admin
from states.States import IDAdmin, new_Car


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "я начал работать")

        except Exception as err:
            logging.exception(err)


@dp.message_handler(Command('admin'))
async def admins_not(message: types.Message):
    admin = admins
    user_id = message.from_user.id
    admin_table = db.select_all_admins_id()
    admins_bot = [user[0] for user in admin_table]

    if user_id in admin or user_id in admins_bot:
        await message.answer(
            "Привествую вас оо все могучий 💪💪💪", reply_markup=adminMarkup
        )

    else:
        await message.answer("У вас нет права админа😬!!!")


@dp.message_handler(text='Новое(🛣,user,driver,new Admin)')
async def new_user_line_driver(message: types.Message):
    await message.answer("Выберите кого хотели добавить", reply_markup=newMarkup)


@dp.message_handler(text='◀️Назад')
async def back_to(message: types.Message):
    await message.answer("◀️", reply_markup=adminMarkup)


@dp.message_handler(text='🙍🏻‍♀️/🙎🏽‍♂️Пассажиры')
async def users_get(message: types.Message):
    users = get_users()
    if len(users) == 0:
        await message.answer("Пока что , в этом направление нет пассажиров")

    for user in users:
        await message.answer(
            f"<b>все данные  </b>\n<b>id :  </b>{user.id}\n"
            f"<b>Фамилия : </b>{user.first_name} \n"
            f"<b>Имя : </b>{user.last_name} \n"
            f"<b>Телефон номер: </b>{user.phone_number} \n "
            f"<b>Имя линии:  </b>{user.name_line}"

        )


@dp.message_handler(text='🏎Водители')
async def drivers_get(message: types.Message):
    users = get_drivers()
    if len(users) == 0:
        await message.answer("Пока что , нет водителя")

    for user in users:
        await message.answer(
            f"<b>все данные  </b>\n<b>id :  </b>{user.user_id}\n<b>Ф.И.О : </b>{user.FIO} "
            f"\n<b>Паспорт серия и номер : </b>{user.ser_num_passport} \n<b>Телефон номер:    </b>{user.phone_number}  "
        )


@dp.message_handler(text="🙍🏻‍♀️/🙎🏽‍♂️User")
async def admin_adduser(message: types.Message):
    await message.answer(
        "Введите ID пользователя: ", reply_markup=ReplyKeyboardRemove()
    )
    await IDAdmin.I1.set()


@dp.message_handler(state=IDAdmin.I1)
async def id_user(message: types.Message, state: FSMContext):
    answer = int(message.text)
    isregis = "not registered"
    db.create_table_users()
    db.admin_add_users(answer, isregis)
    await message.answer("Успешно добавлена", reply_markup=newMarkup)
    await state.reset_state()


@dp.message_handler(text="🙍‍♂️Driver")
async def admin_add_driver(message: types.Message):
    await message.answer(
        "Введите ID пользователя: ", reply_markup=ReplyKeyboardRemove()
    )
    await Id_driver.Ad1.set()


@dp.message_handler(state=Id_driver.Ad1)
async def id_user(message: types.Message, state: FSMContext):
    answer = int(message.text)
    isregis = "not registered"
    db.create_table_drivers()
    db.admin_add_drivers(answer, isregis)
    await state.update_data(user_id=answer)
    await message.answer("Успешно добавлена", reply_markup=newMarkup)
    await state.reset_state()


@dp.message_handler(text="new Admin")
async def admin_add_admin(message: types.Message):
    await message.answer(
        "Введите ID пользователя: ", reply_markup=ReplyKeyboardRemove()
    )
    await New_admin.N1.set()


@dp.message_handler(state=New_admin.N1)
async def id_admin_(message: types.Message, state: FSMContext):
    answer = int(message.text)
    db.create_table_admins()
    db.admin_add_Admin(answer)
    await message.answer("Успешно добавлена", reply_markup=newMarkup)
    await state.reset_state()


@dp.message_handler(text="🚘Машины🚘")
async def get_admin(message: types.Message):
    await message.answer("Выберите Бензин или Газ машины ? ", reply_markup=oil_car1)


@dp.callback_query_handler(text_contains="Gas")
async def get_gas_cars(call: CallbackQuery):
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    cars = get_gas()
    if len(cars) == 0:
        await call.message.answer("Пока что нет таких машин ")

    # права серия номера,марко автомобилья,номер автомобил,тех паспорт,расход,user_id

    for car in cars:
        await call.message.answer(
            f"<b>все данные  </b>\n<b>Водительская удостоверения : </b>{car.ser_num_prava}\n"
            f"<b>Марка автомобиля : </b>  {car.mark_avto}\n "
            f"<b>Номер автомобиля : </b>  {car.number_avto}\n "
            f"<b>Тех.Пасспорт : </b>    {car.ser_num_texpas}\n"
            f"<b>Расход на 100 км : </b>  {car.km_consumption}\n"
            f"<b>ID пользователя: </b>  {car.user_id} \n"
        )


@dp.callback_query_handler(text_contains="PetroL")
async def get_petrol_cars(call: CallbackQuery):
    await call.answer(cache_time=20)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    cars = get_petrol()
    if len(cars) == 0:
        await call.message.answer("Пока что нет таких машин ")

    # права серия номера,марко автомобилья,номер автомобил,тех паспорт,расход,user_id

    for car in cars:
        await call.message.answer(
            f"<b>все данные  </b>\n<b>Водительская удостоверения : </b>{car.ser_num_prava}\n"
            f"<b>Марка автомобиля : </b> {car.mark_avto}\n "
            f"<b>Номер автомобиля : </b> {car.number_avto}\n "
            f"<b>Тех.Пасспорт : </b> {car.ser_num_texpas}\n"
            f"<b>ID пользователя: </b>{car.user_id} \n"
            f"<b>Расход на 100 км : </b> {car.km_consumption}"

        )


@dp.message_handler(text="🏎Car")
async def new_car(message: types.Message):
    await message.answer("Введите ID пользователя: ", reply_markup=ReplyKeyboardRemove())
    await new_Car.NC1.set()


@dp.message_handler(state=new_Car.NC1)
async def id_car_(message: types.Message, state: FSMContext):
    answer = int(message.text)
    db.create_table_cars()
    regis = "not registered"
    db.admin_add_cars(answer, regis)
    await message.answer("Успешно добавлена", reply_markup=newMarkup)
    await state.reset_state()


@dp.message_handler(text='Отчеты & Тех.Проблемы')
async def report_driver(message: types.Message):
    await message.answer("Выберите что хотели узнать", reply_markup=SettingMarkup)


@dp.message_handler(text='🧾Отчет(ВСЕ)')
async def order_day(message: types.Message):
    orders = get_orders()
    if len(orders) == 0:
        await message.answer("Пока что нет таких машин ")

    # права серия номера,марко автомобилья,номер автомобил,тех паспорт,расход,user_id

    for order in orders:
        await message.answer(
            f"<b>все данные 🔽🔽🔽 </b>\n"
            f"<b>ID Отчета: </b>{order.user_id} \n"
            f"<b>ID пользователя: </b>{order.user_id} \n"
            f"<b>Дата отчета : </b> {order.date_day}"
            f"<b>Сколько проехали км : </b> {order.count_day}"
            f"<b>Куда ходили ? : </b>{order.view_road} \n"
            f"<b>Расход топлива л/m³ : </b>{order.oil_day} \n"
        )



@dp.message_handler(text='⚙️Тех.Проблемы(admin)')
async def select_prob(message: types.Message):
    problems = get_problems()
    if len(problems) == 0:
        await message.answer("Пока что нет таких машин ")

    # права серия номера,марко автомобилья,номер автомобил,тех паспорт,расход,user_id

    for problem in problems:
        await message.answer(
            f"<b>все данные 🔽🔽🔽 </b>\n"
            f"<b>ID пользователя: </b>{problem.user_id} \n"
            f"<b>Названия проблемы : </b> {problem.tex_problem} \n"
            f"<b>Описание проблемы : </b> {problem.description} \n"

        )


@dp.message_handler(text='⛽️Топлива')
async def select_fuel(message: types.Message):
    problems = get_FUEL()
    if len(problems) == 0:
        await message.answer("Пока что нет таких машин ")

    # права серия номера,марко автомобилья,номер автомобил,тех паспорт,расход,user_id

    for problem in problems:
        await message.answer(
            f"<b>все данные 🔽🔽🔽 </b>\n"
            f"<b>ID пользователя: </b>{problem.user_id} \n"
            f"<b>Топлива : </b> {problem.fuel} \n"
            f"<b>Вид топлива: </b> {problem.fuel_name} \n"

        )
