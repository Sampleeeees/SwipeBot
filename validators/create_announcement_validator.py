from typing import Union

import httpx
from aiogram.types import PhotoSize
from aiogram.utils.i18n import gettext as _
from services.api_client import UserAPIClient

def balcony_validator(balcony: str) -> bool:
    """
    Валідація чи користувач обрав варіант з кнопок чи вводить відповідь вручну яка не відноситься до значень
    """
    if balcony in [_('Так'), _('Ні')]:
        return True
    return False

def living_condition_validator(condition: str) -> bool:
    """
    Перевірка чи користувач обрав дані з клавіатури або ввів вірно сам чи вводить щось інше
    :param condition: Текст який прийшов від користувача
    :return: Повернення булевого значення
    """
    if condition in [_('Чорнова'), _('Потрібен ремонт'), _('В жилому стані')]:
        return True
    return False

def planning_validator(planning: str) -> bool:
    """
    Перевірка чи користувач обрав дані з клавіатури або ввів вірно сам чи вводить щось інше
    :param planning: Текст який користувач надіслав
    :return: Повернення булевого значення
    """
    if planning in [_('Студія-санвузол'), _('Студія')]:
        return True
    return False

async def house_validate(house_name: str, user_id: int):
    user = UserAPIClient(user=user_id)
    houses = await user.get_houses()
    for house in houses:
        if house_name == house['name']:
            return house['id']
    return False

async def section_validate(house_name: str, section_name: str, user_id: int):
    user = UserAPIClient(user=user_id)
    sections = await user.get_house_sections()
    for section in sections:
        if section['house'] == house_name:
            if section_name == section['name']:
                return section['id']
    return False

async def corps_validate(house_name: str, corps_name: str, user_id: int):
    user = UserAPIClient(user=user_id)
    corps = await user.get_house_corps()
    for corp in corps:
        if corp['house'] == house_name:
            if corps_name == corp['name']:
                return corp['id']
    return False

async def floor_validate(house_name: str, floor_name: str, user_id: int):
    user = UserAPIClient(user=user_id)
    floors = await user.get_house_floors()
    for floor in floors:
        if floor['house'] == house_name:
            if floor_name == floor['name']:
                return floor['id']
    return False


def room_count_validate(count: str) -> bool:
    if count.isdigit() and 1 <= int(count) <= 7:
        return True
    return False

def price_validate(price: str) -> bool:
    if price.isdigit() and 10000 <= int(price) <= 100000000:
        return True
    return False

def area_validate(area: str) -> bool:
    if area.isdigit() and 10 <= int(area) <= 250:
        return True
    return False

def kitchen_area_validate(area: str, kitchen_area: str) -> bool:
    max_area_kitchen = int(area) / 2
    if kitchen_area.isdigit() and 1 <= int(kitchen_area) <= max_area_kitchen:
        return True
    return False

def commission_validate(commission: str, price: str) -> bool:
    max_commission = 70 * int(price) // 100
    if 10 <= int(commission) <= max_commission and commission.isdigit():
        return True
    return False

def photo_validate(photo: PhotoSize) -> bool:
    if photo.width <= 1280 and photo.height <= 720 and photo.file_size <= 19900000:
        return True
    return False



