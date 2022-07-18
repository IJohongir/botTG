from aiogram.dispatcher.filters.state import StatesGroup, State


class Line_edu(StatesGroup):
    LE1 = State()
    LE2 = State()
    LE3 = State()
    LE4 = State()
    LE5 = State()


class Line_OTHER(StatesGroup):
    LO1 = State()
    LO2 = State()
    LO3 = State()
    LO4 = State()
    LO5 = State()


class Tex_problem(StatesGroup):
    TP1 = State()
    TP2 = State()


class reg_oil(StatesGroup):
    ro1 = State()
    ro2 = State()


class Reg_petrol(StatesGroup):
    PR1 = State()
    PR2 = State()
    PR3 = State()
