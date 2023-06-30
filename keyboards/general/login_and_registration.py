from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

def login_register_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Вхід')
    kb.button(text='Реєстрація')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Відмінити")
    return kb.as_markup(resize_keyboard=True)