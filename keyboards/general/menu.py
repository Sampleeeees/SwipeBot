from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Оголошення')
    kb.button(text='Створити оголошення')
    kb.button(text='Профіль')
    kb.button(text='Мова')
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)


def general_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Головне мееню')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)