import httpx
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup
from services.api_client import UserAPIClient
from aiogram.utils.i18n import gettext as _

async def house_kb(user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    user = UserAPIClient(user=user_id)
    houses = await user.get_houses()
    for house in houses:
        kb.button(text=house.get('name'))
    kb.button(text=_('Відмінити'))
    kb.adjust(len(houses), 1)
    return kb.as_markup(resize_keyboard=True)

async def section_kb(house_name: str, user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    user = UserAPIClient(user=user_id)
    sections = await user.get_house_sections()
    for section in sections:
        if section['house'] == house_name:
            kb.button(text=section['name'])
    kb.button(text=_('Назад'))
    kb.adjust(len(sections), 1)
    return kb.as_markup(resize_keyboard=True)

async def corps_kb(house_name: str, user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    user = UserAPIClient(user=user_id)
    corps = await user.get_house_corps()
    for corp in corps:
        if corp['house'] == house_name:
            kb.button(text=corp['name'])
    kb.button(text=_('Назад'))
    kb.adjust(len(corps), 1)
    return kb.as_markup(resize_keyboard=True)

async def floor_kb(house_name: str, user_id: int) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    user = UserAPIClient(user=user_id)
    floors = await user.get_house_floors()
    for floor in floors:
        if floor['house'] == house_name:
            kb.button(text=floor['name'])
    kb.button(text=_('Назад'))
    kb.adjust(len(floors), 1)
    return kb.as_markup(resize_keyboard=True)



def balcony_bool() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Так'))
    kb.button(text=_('Ні'))
    kb.button(text=_('Назад'))
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)

def living_condition_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Чорнова'))
    kb.button(text=_('Потрібен ремонт'))
    kb.button(text=_('В жилому стані'))
    kb.button(text=_('Назад'))
    kb.adjust(3, 1)
    return kb.as_markup(resize_keyboard=True)

def planning_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Студія-санвузол'))
    kb.button(text=_('Студія'))
    kb.button(text=_('Назад'))
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)


def request_location_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Надіслати геолокацію'), request_location=True)
    kb.button(text=_('Назад'))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def back_create_announcement() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Назад'))
    return kb.as_markup(resize_keyboard=True)

def edit_announcement_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Редагувати будинок'))
    kb.button(text=_('Редагувати секцію'))
    kb.button(text=_('Редагувати корпус'))
    kb.button(text=_('Редагувати поверх'))
    kb.button(text=_('Редагувати к-сть кімнат'))
    kb.button(text=_('Редагувати ціну'))
    kb.button(text=_('Редагувати площу'))
    kb.button(text=_('Редагувати площу кухні'))
    kb.button(text=_('Редагувати балкон'))
    kb.button(text=_('Редагувати комісію'))
    kb.button(text=_('Редагувати вулицю'))
    kb.button(text=_('Редагувати район'))
    kb.button(text=_('Редагувати стан'))
    kb.button(text=_('Редагувати планування'))
    kb.button(text=_('Редагувати схему'))
    kb.button(text=_('Редагувати фото'))
    kb.button(text=_('Редагувати локацію'))
    kb.button(text=_('Відмінити'))
    kb.button(text=_('Створити'))
    kb.adjust(4, 4, 4, 4, 1, 2)
    return kb.as_markup(resize_keyboard=True)

