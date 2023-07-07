from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from database.database import set_language_user_db
from keyboards.general.language import language_kb
from keyboards.general.menu import main_kb, back_en_kb, back_uk_kb
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from states.login_state import MenuState

router = Router()

class LanguageStates(StatesGroup):
    check = State()


@router.message(MenuState.menu, F.text == __('Мова'))
async def select_language(message: types.Message, state: FSMContext):
    await message.answer(_('Оберіть мову'),
                         reply_markup=language_kb())
    await state.set_state(LanguageStates.check)\



@router.message(LanguageStates.check, F.text)
async def cmd_set_language_user_db(message: types.Message, state: FSMContext):
    if message.text == 'Українська':
        await set_language_user_db(message.from_user.id, 'uk')
        await state.set_state(LanguageStates.check)
        await message.answer('Дякую', reply_markup=back_uk_kb())
    elif message.text == 'English':
        await set_language_user_db(message.from_user.id, 'en')
        await state.set_state(LanguageStates.check)
        await message.answer('Thanks.', reply_markup=back_en_kb())
    elif message.text == 'Назад':
        await message.answer(_('Ви повернулися до головного меню'),
                             reply_markup=main_kb())
        await state.set_state(MenuState.menu)
    elif message.text == 'Back':
        await message.answer(_('Ви повернулися до головного меню'),
                             reply_markup=main_kb())
        await state.set_state(MenuState.menu)
    else:
        await message.answer(_('Оберіть мову з клавіатури нижче'), reply_markup=language_kb())