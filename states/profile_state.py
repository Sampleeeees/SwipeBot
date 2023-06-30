from aiogram.fsm.state import State, StatesGroup


class ProfileState(StatesGroup):
    my_profile = State()

class AnnouncementState(StatesGroup):
    announ = State()