import httpx
from aiogram import Router, types, Bot, F
from aiogram.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from services.api_client import UserAPIClient, is_authenticated
import states.login_state
from database.users import User
import json
import html
from config.config_reader import config
from keyboards.general.login_and_registration import login_register_kb, cancel_kb
from keyboards.general.menu import main_kb
from keyboards.general.profile import profile_menu_kb, general_profile_menu_kb
from validators.check_input_email import is_valid_email
from states.profile_state import ProfileState
from states.announ_create import AnnouncementCreateState
from handlers.start import url
router = Router()

@router.message(Text('Профіль'))
async def cmd_profile(message: types.Message, state: FSMContext):
    new = await state.set_state(ProfileState.my_profile)
    print(new)
    await message.answer(
        text=f'Привіт {message.from_user.full_name} ти перейшов в меню профілю',
        reply_markup=profile_menu_kb()
    )

@router.message(ProfileState.my_profile, F.text == 'Відмінити')
async def cmd_cancel_profile(message: types.Message, state: FSMContext):
    current = await state.get_state()
    await state.clear()
    print('Cancel', current)
    await message.answer(
        text='Ти тепер в головному меню',
        reply_markup=main_kb()
    )

@router.message(ProfileState.my_profile, F.text == 'Мій профіль')
async def my_profile(message: types.Message, state: FSMContext):
    current = await state.get_state()
    print(current)
    user_id = message.from_user.id
    user = UserAPIClient(user_id)
    if is_authenticated(user_id=user_id):
        data = await user.profile()
        print(data)
        await message.answer(
            f'Telegram: <b>@{message.from_user.username}</b> \n'
            f"Ім'я та прізвище: <b>{data.get('name')} {data.get('surname')}</b>\n"
            f"Пошта: <b>{data.get('email')}</b>\n"
            f'Номер телефону: <b>{data.get("phone_number")}</b> \n'
            f'Роль: <b>{data.get("role").get("name_role")}</b>',
            reply_markup=general_profile_menu_kb(), parse_mode='HTML'
        )
    else:
        await message.answer('Будь-ласка увійдіть в профіль або зареєструйтесь',
                             reply_markup=login_register_kb())
        await state.clear()

@router.message(ProfileState.my_profile, F.text == 'Головне меню')
async def cmd_general_menu(message: types.Message, state: FSMContext):
    currrent = await state.get_state()
    print(currrent)
    await state.clear()
    await message.answer('Ви перейшли до головного меню', reply_markup=main_kb())

@router.message(ProfileState.my_profile, F.text == 'Меню профілю')
async def cmd_menu_profile(message: types.Message, state: FSMContext):
    current = await state.get_state()
    print('Menu_profile', current)
    await state.clear()
    await message.answer('Ви перейшли до меню профілю', reply_markup=profile_menu_kb())
    await state.set_state(ProfileState.my_profile)

