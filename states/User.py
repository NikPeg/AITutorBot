from aiogram.dispatcher.filters.state import State, StatesGroup


class User_(StatesGroup):
    name = State()
    question = State()
    task = State()
    teacher = State()
