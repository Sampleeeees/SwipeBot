from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.i18n import gettext as _

def profile_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_("Мій профіль"))
    kb.button(text=_("Мої оголошення"))
    kb.button(text=_("Відмінити"))
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)

def general_profile_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Головне меню'))
    kb.button(text=_('Меню профілю'))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)