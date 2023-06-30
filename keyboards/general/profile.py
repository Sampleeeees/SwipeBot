from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup

def profile_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Мій профіль")
    kb.button(text="Мої оголошення")
    kb.button(text="Відмінити")
    kb.adjust(2, 1)
    return kb.as_markup(resize_keyboard=True)

def general_profile_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Головне меню')
    kb.button(text='Меню профілю')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)