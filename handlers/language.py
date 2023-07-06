from aiogram import Router, F, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database.database import set_language_user_db
from keyboards.general.language import language_kb
from keyboards.general.menu import main_kb
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from middleware.locale import  Localization

from states.login_state import MenuState

router = Router()

class LanguageStates(StatesGroup):
    check = State()


@router.message(MenuState.menu, F.text == __('Мова'))
async def select_language(message: types.Message, state: FSMContext):
    await message.answer(_('Оберіть мову'),
                         reply_markup=language_kb())
    await state.set_state(LanguageStates.check)

@router.message(LanguageStates.check, F.text)
async def cmd_set_language_user_db(message: types.Message, state: FSMContext):
    if message.text == 'Українська':
        await set_language_user_db(message.from_user.id, 'uk')
        await state.clear()
        await message.answer('Дякую. Перезапустіть бота за допомогою команди /start')
    elif message.text == 'English':
        await set_language_user_db(message.from_user.id, 'en')
        await state.clear()
        await message.answer('Thanks. Restart bot /start')
    else:
        await message.answer('Оберіть мову з клавіатури нижче', reply_markup=language_kb())