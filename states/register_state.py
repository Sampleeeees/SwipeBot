from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    email = State()
    name = State()
    surname = State()
    password1 = State()
    password2 = State()
    edit = State()
    email_edit = State()
    name_edit = State()
    surname_edit = State()
    password1_edit = State()
    password2_edit = State()