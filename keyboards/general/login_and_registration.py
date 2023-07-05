from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _

def login_register_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Вхід')
    kb.button(text='Реєстрація')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def log_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Вхід')
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Відмінити")
    return kb.as_markup(resize_keyboard=True)

def edit_register_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Редагувати email')
    kb.button(text="Редагувати ім'я")
    kb.button(text='Редагувати прізвище')
    kb.button(text='Редагувати пароль')
    kb.button(text='Відмінити')
    kb.button(text='Зареєструватися')
    kb.adjust(4, 2)
    return kb.as_markup(resize_keyboard=True)
