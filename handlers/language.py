from aiogram import Router, F, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database.database import set_language_user_db
from keyboards.general.language import language_kb
from keyboards.general.menu import main_kb

router = Router()

class LanguageStates(StatesGroup):
    check = State()


@router.message(Text('Мова'))
async def select_language(message: types.Message, state: FSMContext):
    await message.answer('Оберіть мову',
                         reply_markup=language_kb())
    await state.set_state(LanguageStates.check)

@router.message(LanguageStates.check, F.text)
async def cmd_set_language_user_db(message: types.Message, state: FSMContext):
    if message.text == 'Українська':
        await state.clear()
        await set_language_user_db(message.from_user.id, 'uk')
        await message.answer('Мову змінено', reply_markup=main_kb())
    elif message.text == 'English':
        await state.clear()
        await set_language_user_db(message.from_user.id, 'en')
        await message.answer('Language switch', reply_markup=main_kb())
    else:
        await message.answer('Оберіть мову з клавіатури нижче')