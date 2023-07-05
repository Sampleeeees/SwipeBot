import httpx
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from services.api_client import UserAPIClient

async def house_kb(user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    user = UserAPIClient(user=user_id)
    houses = await user.get_houses()
    for house in houses:
        kb.button(text=house.get('name'))
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)

async def section_kb(house_name: str, user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    user = UserAPIClient(user=user_id)
    sections = await user.get_house_sections()
    for section in sections:
        if section['house'] == house_name:
            kb.button(text=section['name'])
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)

async def corps_kb(house_name: str, user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    user = UserAPIClient(user=user_id)
    corps = await user.get_house_corps()
    for corp in corps:
        if corp['house'] == house_name:
            kb.button(text=corp['name'])
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)

async def floor_kb(house_name: str, user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    user = UserAPIClient(user=user_id)
    floors = await user.get_house_floors()
    for floor in floors:
        if floor['house'] == house_name:
            kb.button(text=floor['name'])
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)



def balcony_bool() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Так')
    kb.button(text='Ні')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def living_condition_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Чорнова')
    kb.button(text='Потрібен ремонт')
    kb.button(text='В жилому стані')
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)

def planning_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Студія-санвузол')
    kb.button(text='Студія')
    return kb.as_markup(resize_keyboard=True)


def request_location_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Надіслати геолокацію', request_location=True)
    return kb.as_markup(resize_keyboard=True)


def edit_announcement_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Редагувати будинок')
    kb.button(text='Редагувати секцію')
    kb.button(text='Редагувати корпус')
    kb.button(text='Редагувати поверх')
    kb.button(text='Редагувати к-сть кімнат')
    kb.button(text='Редагувати ціну')
    kb.button(text='Редагувати площу')
    kb.button(text='Редагувати площу кухні')
    kb.button(text='Редагувати балкон')
    kb.button(text='Редагувати комісію')
    kb.button(text='Редагувати вулицю')
    kb.button(text='Редагувати район')
    kb.button(text='Редагувати стан')
    kb.button(text='Редагувати планування')
    kb.button(text='Редагувати схему')
    kb.button(text='Редагувати фото')
    kb.button(text='Редагувати локацію')
    kb.button(text='Відмінити')
    kb.button(text='Створити')
    kb.adjust(4, 4, 4, 4, 1, 2)
    return kb.as_markup(resize_keyboard=True)

