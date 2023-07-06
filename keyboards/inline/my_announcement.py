from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

class MyAnnouncementCallbackFactory(CallbackData, prefix='my_announcement'):
    name: str
    pk: int

def inline_my_announcement_kb(flat_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=_('Редагувати'), callback_data=MyAnnouncementCallbackFactory(name='edit_my_announcement', pk=flat_id))
    kb.button(text=_('Показати геолокацію'), callback_data='show_location')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)