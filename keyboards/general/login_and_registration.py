from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

def login_register_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Вхід'))
    kb.button(text=_('Реєстрація'))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def log_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Вхід'))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_("Відмінити"))
    return kb.as_markup(resize_keyboard=True)

def edit_register_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Редагувати email'))
    kb.button(text=_("Редагувати ім'я"))
    kb.button(text=_('Редагувати прізвище'))
    kb.button(text=_('Редагувати пароль'))
    kb.button(text=_('Відмінити'))
    kb.button(text=_('Зареєструватися'))
    kb.adjust(4, 2)
    return kb.as_markup(resize_keyboard=True)
