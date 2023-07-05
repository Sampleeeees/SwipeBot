from typing import Any

import httpx
from aiogram import Router, types, Bot, F
from aiogram.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from services.api_client import UserAPIClient
from aiogram.utils.i18n import gettext as _
from config.config_reader import config
from keyboards.general.login_and_registration import login_register_kb, cancel_kb
from keyboards.general.menu import main_kb
from validators.check_input_email import is_valid_email
from states.login_state import LoginState
from states.register_state import RegisterStates
url = config.url

access_token = ''

print(url)


router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        _('Вітаю в системі Swipe \n'
        'Увійдіть або зареєструйтесь'),
        reply_markup=login_register_kb()
    )

@router.message(LoginState(), F.text.casefold() == 'відмінити')
async def cmd_cancel(message: types.Message, state: FSMContext) -> Any:
    await state.clear()
    await message.answer(
        _('Вітаю в системі Swipe \n'
        'Увійдіть або зареєструйтесь'),
        reply_markup=login_register_kb()
    )

@router.message(Text('Вхід'))
@router.message(Command('login'))
async def cmd_login(message: types.Message, state: FSMContext) -> None:
    await state.set_state(LoginState.email)
    await message.answer(
        _("Уведіть ваш email"),
        reply_markup=cancel_kb()
    )


@router.message(Text('Реєстрація'))
@router.message(Command('register'))
async def cmd_login(message: types.Message, state: FSMContext) -> None:
    await state.set_state(RegisterStates.email)
    await message.answer(
        _("Уведіть ваш email"),
        reply_markup=cancel_kb()
    )

@router.message(LoginState.email, F.text)
async def cmd_email(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == LoginState.email:
        email = message.text

        if is_valid_email(email):
            await state.update_data(email=email)
            await state.set_state(LoginState.password)
            await message.answer(
                _("Тепер введіть пароль"),
                reply_markup=cancel_kb(),
                input_field_placeholder="Введіть пароль"
            )
        else:
            await message.answer(_('Введіть email будь-ласка '))


@router.message(LoginState.password, F.text)
async def cmd_password(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == LoginState.password:
        password = message.text

        data = await state.update_data(password=password)
        await state.clear()
        print(current_state)
        print(data)
        await message.answer(_('Дякую \n'
                             'Ваші дані: \n'
                             f'Email: {data.get("email")} \n'
                             f'Password: {data.get("password")}'))
        await message.answer(_('Перевіряю введені дані...'), reply_markup=ReplyKeyboardRemove())
        user = UserAPIClient(user=message.from_user.id)
        response = await user.login(data)
        print("Response", response)
        if response:
            await message.answer(
                text=_('Вхід виконано'),
                reply_markup=main_kb()
            )
        else:
            await state.clear()
            await message.answer(
                text=_('Помилка входу. Спробуйте увійти заново вказавші вірні дані.\n'
                     'Якщо не маєте аккаунту то зареєструйтесь (/register)'),
                reply_markup=login_register_kb()
            )

@router.message(LoginState(), F.text)
async def cmd_login_echo(message: types.Message, state: FSMContext):
    await message.answer(_('Оберіть дію'))



