from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Оголошення'))
    kb.button(text=_('Створити оголошення'))
    kb.button(text=_('Профіль'))
    kb.button(text=_('Мова'))
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)

def back_uk_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Назад')
    return kb.as_markup(resize_keyboard=True)

def back_en_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Back')
    return kb.as_markup(resize_keyboard=True)

def general_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=_('Головне меню'))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)