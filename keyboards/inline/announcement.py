from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class AnnouncementCallback(CallbackData, prefix='announcement'):
    step: str
    pk: Optional[int]

def inline_announcement_kb(pk) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Минуле', callback_data=AnnouncementCallback(step='go_previous', pk=pk).pack())
    kb.button(text='Наступне', callback_data=AnnouncementCallback(step='go_next', pk=pk).pack())
    kb.button(text='Показати геолокацію', callback_data=AnnouncementCallback(step='geo', pk=pk).pack())
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)