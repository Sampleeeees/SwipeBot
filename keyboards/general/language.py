from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

def language_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Українська')
    kb.button(text='Англійська')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

