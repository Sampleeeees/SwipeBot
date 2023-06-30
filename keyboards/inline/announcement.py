from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

class AnnouncementCallback(CallbackData, prefix='announcement'):
    go: str
    pk: int

def inline_announcement_kb(pk) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='Минуле', callback_data=AnnouncementCallback(go='go_previous', pk=pk).pack())
    kb.button(text='Наступне', callback_data=AnnouncementCallback(go='go_next', pk=pk).pack())
    kb.button(text='Показати геолокацію', callback_data=AnnouncementCallback(go='geo', pk=pk).pack())
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)