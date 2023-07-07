import httpx
from aiogram import Router, types, Bot, F
from aiogram.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from services.api_client import UserAPIClient, is_authenticated
from aiogram.utils.i18n import gettext as _, get_i18n
from aiogram.utils.i18n import lazy_gettext as __
from keyboards.general.login_and_registration import login_register_kb
from keyboards.general.menu import main_kb
from keyboards.general.profile import profile_menu_kb, general_profile_menu_kb
from states.login_state import LoginState, MenuState
from states.profile_state import ProfileState

router = Router()

@router.message(MenuState.menu, F.text == __('Профіль'))
async def cmd_profile(message: types.Message, state: FSMContext):

    new = await state.set_state(ProfileState.my_profile)
    print(new)
    await message.answer(
        text=_('Привіт {user} ти перейшов в меню профілю').format(user=message.from_user.full_name),
        reply_markup=profile_menu_kb(), locale=get_i18n().current_locale
    )

@router.message(ProfileState.my_profile, F.text == __('Відмінити'))
async def cmd_cancel_profile(message: types.Message, state: FSMContext):
    current = await state.get_state()
    await state.set_state(MenuState.menu)
    print('Cancel', current)
    await message.answer(
        text='Ти тепер в головному меню',
        reply_markup=main_kb()
    )

@router.message(ProfileState.my_profile, F.text == __('Мій профіль'))
async def my_profile(message: types.Message, state: FSMContext):
    current = await state.get_state()
    print(current)
    user_id = message.from_user.id
    user = UserAPIClient(user_id)
    if is_authenticated(user_id=user_id):
        data = await user.profile()
        print(data)
        await message.answer(
            _('Telegram: <b>@{username}</b> \n'
              "Ім'я та прізвище: <b>{name} {surname}</b>\n"
              "Пошта: <b>{email}</b>\n"
              'Номер телефону: <b>{phone_number}</b> \n'
              'Роль: <b>{role}</b>').format(
                username=message.from_user.username,
                name=data.get('name'),
                surname=data.get('surname'),
                email=data.get('email'),
                phone_number=data.get('phone_number'),
                role=data.get('role').get('name_role')
            ),
            reply_markup=general_profile_menu_kb(), parse_mode='HTML'
        )
    else:
        await message.answer(_('Будь-ласка увійдіть в профіль або зареєструйтесь'),
                             reply_markup=login_register_kb())
        await state.clear()

@router.message(ProfileState.my_profile, F.text == __('Головне меню'))
async def cmd_general_menu(message: types.Message, state: FSMContext):
    currrent = await state.get_state()
    print(currrent)
    await state.set_state(MenuState.menu)
    await message.answer(_('Ви перейшли до головного меню'), reply_markup=main_kb())

@router.message(ProfileState.my_profile, F.text == __('Меню профілю'))
async def cmd_menu_profile(message: types.Message, state: FSMContext):
    current = await state.get_state()
    print('Menu_profile', current)
    await message.answer(_('Ви перейшли до меню профілю'), reply_markup=profile_menu_kb())
    await state.set_state(ProfileState.my_profile)

