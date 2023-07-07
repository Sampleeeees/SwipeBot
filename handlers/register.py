from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext

from states.login_state import LoginState
from states.register_state import RegisterStates
from keyboards.general.login_and_registration import cancel_kb, login_register_kb, edit_register_kb, log_kb
from services.api_client import UserAPIClient
from validators.check_input_email import is_valid_email
from validators.register_validator import name_valid, password_valid
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

router = Router()


@router.message(RegisterStates(), F.text == __('Відмінити'))
async def cmd_register_cancel(message: types.Message, state: FSMContext):
    await state.set_state(LoginState.menu)
    await message.answer(
        _('Вітаю в системі Swipe \n'
          'Увійдіть або зареєструйтесь'),
        reply_markup=login_register_kb()
    )

@router.message(RegisterStates.email, F.text)
@router.message(RegisterStates.email_edit, F.text)
async def register_email(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print('Email state', current_state)

    if current_state == RegisterStates.email:
        email = message.text

        if is_valid_email(email):
            await state.update_data(email=email)
            await state.set_state(RegisterStates.name)
            await message.answer(text=_("Тепер введіть ваше ім'я"),
                                 reply_markup=cancel_kb())
        else:
            await message.answer(_('Ви ввели невірний email. Повторіть спробу'))

    elif current_state == RegisterStates.email_edit:
        email = message.text
        if is_valid_email(email):
            data = await state.update_data(email=email)
            await state.set_state(RegisterStates.edit)
            await message.answer(_("Дякую. Ваші дані: \n"
                                   "Пошта: {email} \n"
                                   "Ім'я: {name} \n"
                                   "Прізвище: {surname} \n"
                                   "Пароль 1: {password1} \n"
                                   "Пароль 2: {password2} \n \n"
                                   'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                   'Інакше оберіть що відредагувати'
                                   ).format(email=data.get('email'),
                                            name=data.get('name'),
                                            surname=data.get('surname'),
                                            password1=data.get('password1'),
                                            password2=data.get('password2')),
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer(_('Ви ввели невірний email. Повторіть спробу'))



@router.message(RegisterStates.name, F.text)
@router.message(RegisterStates.name_edit, F.text)
async def register_name(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == RegisterStates.name:
        name = message.text

        if name_valid(name):
            await state.update_data(name=name)
            await state.set_state(RegisterStates.surname)
            await message.answer(text=_("Тепер введіть прізвище"),
                                 reply_markup=cancel_kb())
        else:
            await message.answer(_("Ім'я повинно починатися з великої літери та мати не менше ніж 2 "
                                 'символи та складатися тільки з букв.\n'
                                 "Введіть ваше ім'я"))
    elif current_state == RegisterStates.name_edit:
        name = message.text

        if name_valid(name):
            data = await state.update_data(name=name)
            await state.set_state(RegisterStates.edit)
            await message.answer(_("Дякую. Ваші дані: \n"
                                   "Пошта: {email} \n"
                                   "Ім'я: {name} \n"
                                   "Прізвище: {surname} \n"
                                   "Пароль 1: {password1} \n"
                                   "Пароль 2: {password2} \n \n"
                                   'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                   'Інакше оберіть що відредагувати'
                                   ).format(email=data.get('email'),
                                            name=data.get('name'),
                                            surname=data.get('surname'),
                                            password1=data.get('password1'),
                                            password2=data.get('password2')),
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer(_("Ім'я повинно починатися з великої літери та мати не менше ніж 2 "
                                 'символи та складатися тільки з букв.\n'
                                 "Введіть ваше ім'я"))

@router.message(RegisterStates.surname, F.text)
@router.message(RegisterStates.surname_edit, F.text)
async def register_surname(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == RegisterStates.surname:
        surname = message.text

        if name_valid(surname):
            await state.update_data(surname=surname)
            await state.set_state(RegisterStates.password1)
            await message.answer(text=_("Дякую. Тепер потрібно ввести пароль"),
                                 reply_markup=cancel_kb())
        else:
            await message.answer(_("Прізвище повинно починатися з великої літери та мати не менше ніж 2 "
                                 'символи та складатися тільки з букв.\n'
                                 "Введіть ваше прізвище"))
    elif current_state == RegisterStates.surname_edit:
        surname = message.text

        if name_valid(surname):
            data = await state.update_data(surname=surname)
            await state.set_state(RegisterStates.password1)
            await message.answer(_("Дякую. Ваші дані: \n"
                                   "Пошта: {email} \n"
                                   "Ім'я: {name} \n"
                                   "Прізвище: {surname} \n"
                                   "Пароль 1: {password1} \n"
                                   "Пароль 2: {password2} \n \n"
                                   'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                   'Інакше оберіть що відредагувати'
                                   ).format(email=data.get('email'),
                                            name=data.get('name'),
                                            surname=data.get('surname'),
                                            password1=data.get('password1'),
                                            password2=data.get('password2')),
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer(_("Прізвище повинно починатися з великої літери та мати не менше ніж 2 "
                                 'символи та складатися тільки з букв.\n'
                                 "Введіть ваше прізвище"))


@router.message(RegisterStates.password1, F.text)
@router.message(RegisterStates.password1_edit, F.text)
async def register_password1(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == RegisterStates.password1:
        password1 = message.text

        if password_valid(password1):
            await state.update_data(password1=password1)
            await state.set_state(RegisterStates.password2)
            await message.answer(text=_('Повторіть пароль'),
                                 reply_markup=cancel_kb())
        else:
            await message.answer(_('Пароль повинне бути не менше ніж з 8 символів та містити букви та цифри. \n'
                                 'Введіть пароль ще раз'))
    elif current_state == RegisterStates.password1_edit:
        password1 = message.text

        if password_valid(password1):
            await state.update_data(password1=password1)
            await state.set_state(RegisterStates.password2_edit)
            await message.answer(text=_('Повторіть пароль'),
                                 reply_markup=cancel_kb())
        else:
            await message.answer(_('Пароль повинне бути не менше ніж з 8 символів та містити букви та цифри. \n'
                                 'Введіть пароль ще раз'))


@router.message(RegisterStates.password2, F.text)
@router.message(RegisterStates.password2_edit, F.text)
async def register_password2(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()

    if current_state == RegisterStates.password2:
        password2 = message.text

        data = await state.update_data(password2=password2)
        print('Data:', data)
        print(data.get('password1'))
        if password2 == data.get('password1'):
            await state.set_state(RegisterStates.edit)

            await message.answer(_("Дякую. Ваші дані: \n"
                                   "Пошта: {email} \n"
                                   "Ім'я: {name} \n"
                                   "Прізвище: {surname} \n"
                                   "Пароль 1: {password1} \n"
                                   "Пароль 2: {password2} \n \n"
                                   'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                   'Інакше оберіть що відредагувати'
                                   ).format(email=data.get('email'),
                                            name=data.get('name'),
                                            surname=data.get('surname'),
                                            password1=data.get('password1'),
                                            password2=data.get('password2')),
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer(_('Ваш пароль не співпадає з минулим.\n'
                                 'Введіть пароль повторно'))
    elif current_state == RegisterStates.password2_edit:
        password2 = message.text

        data = await state.update_data(password2=password2)
        if password2 == data.get('password1'):
            await state.set_state(RegisterStates.edit)
            await message.answer(_("Дякую. Ваші дані: \n"
                                   "Пошта: {email} \n"
                                   "Ім'я: {name} \n"
                                   "Прізвище: {surname} \n"
                                   "Пароль 1: {password1} \n"
                                   "Пароль 2: {password2} \n \n"
                                   'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                   'Інакше оберіть що відредагувати'
                                   ).format(email=data.get('email'),
                                            name=data.get('name'),
                                            surname=data.get('surname'),
                                            password1=data.get('password1'),
                                            password2=data.get('password2')),
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer(_('Ваш пароль не співпадає з минулим.\n'
                                 'Введіть пароль повторно'))

@router.message(RegisterStates.edit, F.text)
async def edit_register_data(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()

    if current_state == RegisterStates.edit:
        if message.text == _('Зареєструватися'):
            data = await state.get_data()
            print('Data:', data)
            print(data.get('password1'))
            await state.clear()

            await message.answer(_("Дякую. Ваші дані: \n"
                                     "Пошта: {email} \n"
                                     "Ім'Я: {name} \n"
                                     "Прізвище: {surname} \n"
                                     "Пароль1: {password1} \n"
                                     "Пароль2: {password2}"
                                   ).format(email=data.get('email'),
                                            name=data.get('name'),
                                            surname=data.get('surname'),
                                            password1=data.get('password1'),
                                            password2=data.get('password2')))
            await message.answer(_('Реєструю вас в системі...'))
            user = UserAPIClient(user=message.from_user.id)
            response = await user.register_user(data)
            if response:
                await message.answer(_('Вітаю. Ви зареєстровані.\n'
                                         'Ваші дані для входу: \n'
                                         'Email: {email} \n'
                                         'Password: {password2}\n \n'
                                         '<b>Підтвердіть вашу пошту </b>, щоб мати можливість користуватися ботом \n \n'
                                     'Якщо ви підтвердили пошту тоді можете авторизуватися (/login)').format(email=data.get('email'),
                                                                                                             password2=data.get('password2')),
                                         parse_mode='HTML',
                                     reply_markup=log_kb())
            else:
                await message.answer(_('Упс... Схоже ви вже зареєстровані в системі.\n'
                                         'Спробуй увійти в акаунт (/login) '))
        elif message.text == _('Редагувати email'):
            await state.set_state(RegisterStates.email_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
            await message.answer(_('Введіть новий email'))
        elif message.text == _("Редагувати ім'я"):
            await state.set_state(RegisterStates.name_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_("Введіть нове ім'я"))
        elif message.text == _('Редагувати прізвище'):
            await state.set_state(RegisterStates.surname_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть нове прізвище'))
        elif message.text == _('Редагувати пароль'):
            await state.set_state(RegisterStates.password1_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть новий пароль'))
        elif message.text == _('Відмінити'):
            await state.set_state(LoginState.menu)
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
            await message.answer(_('Ви повернулися до входу'),
                                 reply_markup=login_register_kb())
        else:
            await message.answer(_('Оберіть варіант з клавіатури'),
                                 reply_markup=edit_register_kb())


