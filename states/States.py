from aiogram.dispatcher.filters.state import StatesGroup, State


class UReg(StatesGroup):
    U1 = State()
    U2 = State()
    U3 = State()
    U4 = State()


class Cars_Petrol(StatesGroup):
    Cp1 = State()
    Cp2 = State()
    Cp3 = State()
    Cp4 = State()
    Cp5 = State()
    Cp6 = State()
    Cp7 = State()
    Cp8 = State()


class Cars_Gas(StatesGroup):
    Cg1 = State()
    Cg2 = State()
    Cg3 = State()
    Cg4 = State()
    Cg5 = State()
    Cg6 = State()
    Cg7 = State()
    Cg8 = State()


class new_Car(StatesGroup):
    NC1 = State()


class New_admin(StatesGroup):
    N1 = State()


class IDAdmin(StatesGroup):
    I1 = State()


class Id_driver(StatesGroup):
    Ad1 = State()
    Ad2 = State()
    Ad3 = State()
    Ad4 = State()
    Ad5 = State()
    Ad6 = State()


class Home_loc(StatesGroup):
    H1 = State()
    H2 = State()


class EDU_loc(StatesGroup):
    ED1 = State()
    ED2 = State()


class Other_loc(StatesGroup):
    O1 = State()
    O2 = State()


class RDriver(StatesGroup):
    D1 = State()
    D2 = State()
    D3 = State()
    D4 = State()


class USERS(StatesGroup):
    US1 = State()
