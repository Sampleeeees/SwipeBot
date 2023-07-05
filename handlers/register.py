from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from states.register_state import RegisterStates
from keyboards.general.login_and_registration import cancel_kb, login_register_kb, edit_register_kb, log_kb
from services.api_client import UserAPIClient
from validators.check_input_email import is_valid_email
from validators.register_validator import name_valid, password_valid
from aiogram.utils.i18n import gettext as _

router = Router()


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
            await message.answer('Ви ввели невірний email. Повторіть спробу')

    elif current_state == RegisterStates.email_edit:
        email = message.text
        if is_valid_email(email):
            data = await state.update_data(email=email)
            await state.set_state(RegisterStates.edit)
            await message.answer(f"Дякую. Ваші оновлені дані: \n"
                                 f"Email: {data.get('email')} \n"
                                 f"Name: {data.get('name')} \n"
                                 f"Surname: {data.get('surname')} \n"
                                 f"Password1: {data.get('password1')} \n"
                                 f"Password2: {data.get('password2')} \n \n"
                                 'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                 'Інакше оберіть що відредагувати',
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer('Ви ввели невірний email. Повторіть спробу')


@router.message(RegisterStates(), F.text == 'Відмінити')
async def cmd_register_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Ви повернулися до меню входу в систему',
                         reply_markup=login_register_kb())


@router.message(RegisterStates.name, F.text)
@router.message(RegisterStates.name_edit, F.text)
async def register_name(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == RegisterStates.name:
        name = message.text

        if name_valid(name):
            await state.update_data(name=name)
            await state.set_state(RegisterStates.surname)
            await message.answer(text="Тепер введіть прізвище",
                                 reply_markup=cancel_kb())
        else:
            await message.answer("Ім'я повинно починатися з великої літери та мати не менше ніж 2 "
                                 'символи та складатися тільки з букв.\n'
                                 "Введіть ваше ім'я")
    elif current_state == RegisterStates.name_edit:
        name = message.text

        if name_valid(name):
            data = await state.update_data(name=name)
            await state.set_state(RegisterStates.edit)
            await message.answer(f"Дякую. Ваші оновлені дані: \n"
                                 f"Email: {data.get('email')} \n"
                                 f"Name: {data.get('name')} \n"
                                 f"Surname: {data.get('surname')} \n"
                                 f"Password1: {data.get('password1')} \n"
                                 f"Password2: {data.get('password2')} \n \n"
                                 'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                 'Інакше оберіть що відредагувати',
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer("Ім'я повинно починатися з великої літери та мати не менше ніж 2 "
                                 'символи та складатися тільки з букв.\n'
                                 "Введіть ваше ім'я")

@router.message(RegisterStates.surname, F.text)
@router.message(RegisterStates.surname_edit, F.text)
async def register_surname(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == RegisterStates.surname:
        surname = message.text

        if name_valid(surname):
            await state.update_data(surname=surname)
            await state.set_state(RegisterStates.password1)
            await message.answer(text="Дякую. Тепер потрібно ввести пароль",
                                 reply_markup=cancel_kb())
        else:
            await message.answer("Прізвище повинно починатися з великої літери та мати не менше ніж 2 "
                                 'символи та складатися тільки з букв.\n'
                                 "Введіть ваше прізвище")
    elif current_state == RegisterStates.surname_edit:
        surname = message.text

        if name_valid(surname):
            data = await state.update_data(surname=surname)
            await state.set_state(RegisterStates.password1)
            await message.answer(f"Дякую. Ваші оновлені дані: \n"
                                 f"Email: {data.get('email')} \n"
                                 f"Name: {data.get('name')} \n"
                                 f"Surname: {data.get('surname')} \n"
                                 f"Password1: {data.get('password1')} \n"
                                 f"Password2: {data.get('password2')} \n \n"
                                 'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                 'Інакше оберіть що відредагувати',
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer("Прізвище повинно починатися з великої літери та мати не менше ніж 2 "
                                 'символи та складатися тільки з букв.\n'
                                 "Введіть ваше прізвище")


@router.message(RegisterStates.password1, F.text)
@router.message(RegisterStates.password1_edit, F.text)
async def register_password1(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == RegisterStates.password1:
        password1 = message.text

        if password_valid(password1):
            await state.update_data(password1=password1)
            await state.set_state(RegisterStates.password2)
            await message.answer(text='Повторіть пароль',
                                 reply_markup=cancel_kb())
        else:
            await message.answer('Пароль повинне бути не менше ніж з 8 символів та містити букви та цифри. \n'
                                 'Введіть пароль ще раз')
    elif current_state == RegisterStates.password1_edit:
        password1 = message.text

        if password_valid(password1):
            await state.update_data(password1=password1)
            await state.set_state(RegisterStates.password2_edit)
            await message.answer(text='Повторіть пароль',
                                 reply_markup=cancel_kb())
        else:
            await message.answer('Пароль повинне бути не менше ніж з 8 символів та містити букви та цифри. \n'
                                 'Введіть пароль ще раз')


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

            await message.answer(f"Дякую. Ваші дані: \n"
                                 f"Email: {data.get('email')} \n"
                                 f"Name: {data.get('name')} \n"
                                 f"Surname: {data.get('surname')} \n"
                                 f"Password1: {data.get('password1')} \n"
                                 f"Password2: {data.get('password2')} \n \n"
                                 'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                 'Інакше оберіть що відредагувати',
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer('Ваш пароль не співпадає з минулим.\n'
                                 'Введіть пароль повторно')
    elif current_state == RegisterStates.password2_edit:
        password2 = message.text

        data = await state.update_data(password2=password2)
        if password2 == data.get('password1'):
            await state.set_state(RegisterStates.edit)
            await message.answer(f"Дякую. Ваші дані: \n"
                                 f"Email: {data.get('email')} \n"
                                 f"Name: {data.get('name')} \n"
                                 f"Surname: {data.get('surname')} \n"
                                 f"Password1: {data.get('password1')} \n"
                                 f"Password2: {data.get('password2')} \n \n"
                                 'Якщо все вірно натисніть кнопку <b>Зареєструватися</b> \n'
                                 'Інакше оберіть що відредагувати',
                                 reply_markup=edit_register_kb(),
                                 parse_mode='HTML')
        else:
            await message.answer('Ваш пароль не співпадає з минулим.\n'
                                 'Введіть пароль повторно')

@router.message(RegisterStates.edit, F.text)
async def edit_register_data(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()

    if current_state == RegisterStates.edit:
        if message.text == 'Зареєструватися':
            data = await state.get_data()
            print('Data:', data)
            print(data.get('password1'))
            await state.clear()

            await message.answer(f"Дякую. Ваші дані: \n"
                                     f"Email: {data.get('email')} \n"
                                     f"Name: {data.get('name')} \n"
                                     f"Surname: {data.get('surname')} \n"
                                     f"Password1: {data.get('password1')} \n"
                                     f"Password2: {data.get('password2')}")
            await message.answer('Реєструю вас в системі...')
            user = UserAPIClient(user=message.from_user.id)
            response = await user.register_user(data)
            if response:
                await message.answer(f'Вітаю. Ви зареєстровані.\n'
                                         f'Ваші дані для входу: \n'
                                         f'Email: {data.get("email")} \n'
                                         f'Password: {data.get("password2")}\n \n'
                                         f'<b>Підтвердіть вашу пошту </b>, щоб мати можливість користуватися ботом \n \n'
                                     f'Якщо ви підтвердили пошту тоді можете авторизуватися (/login)',
                                         parse_mode='HTML',
                                     reply_markup=log_kb())
            else:
                await message.answer('Упс... Схоже ви вже зареєстровані в системі.\n'
                                         'Спробуй увійти в акаунт (/login) ')
        elif message.text == 'Редагувати email':
            await state.set_state(RegisterStates.email_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id-1)
            await message.answer('Введіть новий email')
        elif message.text == "Редагувати ім'я":
            await state.set_state(RegisterStates.name_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer("Введіть нове ім'я")
        elif message.text == 'Редагувати прізвище':
            await state.set_state(RegisterStates.surname_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer('Введіть нове прізвище')
        elif message.text == 'Редагувати пароль':
            await state.set_state(RegisterStates.password1_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer('Введіть новий пароль')
        elif message.text == '':
            await state.clear()
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id - 1)
            await message.answer('Ви повернулися до входу',
                                 reply_markup=login_register_kb())
        else:
            await message.answer('Оберіть варіант з клавіатури',
                                 reply_markup=edit_register_kb())


