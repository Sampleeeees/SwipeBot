from aiogram.fsm.state import StatesGroup, State

class LoginState(StatesGroup):
    email = State()
    password = State()