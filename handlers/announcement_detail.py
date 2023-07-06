import base64
import os
from contextlib import suppress
from aiogram import F, Router, types, Bot
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, URLInputFile, FSInputFile
from keyboards.general.menu import main_kb
from states.announ_edit import MyAnnouncementEditState
from states.profile_state import AnnouncementState, ProfileState
from services.api_client import AnnouncementAPIClient, UserAPIClient
from keyboards.inline.my_announcement import inline_my_announcement_kb, MyAnnouncementCallbackFactory
from keyboards.general.announcement import edit_announcement_kb, request_location_kb, planning_kb, living_condition_kb, \
    balcony_bool, floor_kb, corps_kb, section_kb, house_kb
from validators.create_announcement_validator import photo_validate, planning_validator, living_condition_validator, \
    commission_validate, balcony_validator, kitchen_area_validate, area_validate, price_validate, room_count_validate, \
    floor_validate, corps_validate, section_validate, house_validate

DEFAULT_IMAGE = 'https://volynonline.com/wp-content/uploads/2023/05/k35l7m-0x0-9600x5400-6ytrqy7nb2qsb6b4jakz3k6ziajentde.jpg'


router = Router()

user_data = {}

def default_image(url=None):
    image = URLInputFile(
        DEFAULT_IMAGE,
        filename='default_image.png'
    )
    if url:
        image.url = url
    return image

async def get_full_flat_data(user_id, flat_id):
    user = AnnouncementAPIClient(user_id)
    flat = await user.get_flat(flat_id)
    print('Flat', flat)
    house_id = flat['house']
    house = await user.get_house(house_id)
    print("HOUSE", house)
    section_id = flat['section']
    floor_id = flat['floor']
    corps_id = flat['corps']
    section = await user.get_section(section_id)
    floor = await user.get_floor(floor_id)
    corps = await user.get_corps(corps_id)

    data = {
        'house': flat['house'],
        'house_name': house,
        'section': section['id'],
        'section_name': section['name'],
        'corps': corps['id'],
        'corps_name': corps['name'],
        'floor': floor['id'],
        'floor_name': floor['name'],
        'room_amount': flat['room_amount'],
        'price': flat['price'],
        'square': flat['square'],
        'kitchen_square': flat['kitchen_square'],
        'balcony': flat['balcony'],
        'balcony_name': 'Так' if flat['balcony'] else 'Ні',
        'commission': flat['commission'],
        'district': flat['district'],
        'micro_district': flat['micro_district'],
        'living_condition': flat['living_condition'],
        'living_condition_name': 'Чорнова' if flat['living_condition'] == 'draft' else 'Потрібен ремонт' if flat['living_condition'] == 'repair' else 'В жилому стані',
        'planning': flat['planning'],
        'planning_name': 'Студія' if flat['planning'] == 'studio' else 'Студія-санвузел' if flat['planning'] == 'studio-bathroom' else 'Не вказано',
        'scheme': flat['scheme']
    }
    return data

async def get_image(path=None):
    image = URLInputFile(url=str(path), filename='image.png')
    return image


@router.message(ProfileState.my_profile, F.text == __('Мої оголошення'))
async def cmd_list_announcement(message: types.Message, state: FSMContext):
    await state.set_state(ProfileState.my_profile)
    user_id = message.from_user.id
    user = AnnouncementAPIClient(user_id)
    user_data[user_id] = 0
    list_announce = await user.list_announcement()
    print("LIST", list_announce)
    if list_announce:
        for announ in list_announce:
            print('ANNOUCEMENT', announ)
            flat_id = announ['flat']
            data = await get_full_flat_data(message.from_user.id, flat_id)
            await message.answer_photo(photo=await get_image(data["scheme"]), caption=f'Будинок: {data["house_name"]} \n'
                                     f'Секція: {data["section_name"]}\n'
                                     f'Поверх: {data["floor_name"]}\n'
                                     f'Корпус: {data["corps_name"]}\n'
                                     f'К-сть кімнат: {data["room_amount"]}\n'
                                     f'Ціна: {data["price"]}\n'
                                     f'Площа: {data["square"]}\n'
                                     f'Площа кухні: {data["kitchen_square"]}\n'
                                     f'Балкон: {data["balcony_name"]}\n'
                                     f'Комісія: {data["commission"]}\n'
                                     f'Вулиця: {data["district"]}\n'
                                     f'Район: {data["micro_district"]}\n'
                                     f'Стан: {data["living_condition_name"]}\n'
                                     f'Планування: {data["planning_name"]}\n',
                                 reply_markup=inline_my_announcement_kb(flat_id))

    else:
        await message.answer(_('У вас немає жодного створеного оголошення'))

@router.callback_query(Text('show_location'))
async def my_announcement_show_location(callback: CallbackQuery):
    await callback.message.answer_location(
        latitude=46.4313303, longitude=30.7100851
    )
    await callback.answer()

@router.callback_query(MyAnnouncementCallbackFactory.filter(F.name == 'edit_my_announcement'))
async def my_announcement_edit(callback: CallbackQuery, state: FSMContext, callback_data: MyAnnouncementCallbackFactory, bot: Bot):
    data = await get_full_flat_data(callback.from_user.id, callback_data.pk)
    await state.update_data(data=data)
    print(data)
    down_photo = await get_image(data['scheme'])
    message = await bot.send_photo(chat_id=callback.message.chat.id, photo=down_photo)
    photo = message.photo[-1]
    await bot.delete_message(chat_id=callback.message.chat.id, message_id=message.message_id)
    file = await bot.get_file(photo.file_id)
    filename, file_extension = os.path.splitext(file.file_path)
    src = 'media/announcement/' + file.file_id + file_extension
    await bot.download_file(file_path=file.file_path, destination=src)
    data['id'] = callback_data.pk
    data['general_src'] = src
    data['scheme'] = decode_image(src, file_extension)
    print(data['scheme'])
    await callback.message.answer_photo(
        photo=FSInputFile(data.get('general_src')),
        caption=_(
            "Будинок: {house_name}\n"
            "Секція: {section_name}\n"
            "Корпус: {corps_name}\n"
            "Поверх: {floor_name}\n"
            "К-сть кімнат: {room_amount}\n"
            "Ціна: {price}\n"
            "Площа: {square}\n"
            "Площа кухні: {kitchen_square}\n"
            "Балкон: {balcony_name}\n"
            "Вулиця: {district}\n"
            "Район: {micro_district}\n"
            "Стан: {living_condition_name}\n"
            "Планування: {planning_name}\n\n"
            "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
        ).format(
            house_name=data.get('house_name'),
            section_name=data.get('section_name'),
            corps_name=data.get('corps_name'),
            floor_name=data.get('floor_name'),
            room_amount=data.get('room_amount'),
            price=data.get('price'),
            square=data.get('square'),
            kitchen_square=data.get('kitchen_square'),
            balcony_name=data.get('balcony_name'),
            district=data.get('district'),
            micro_district=data.get('micro_district'),
            living_condition_name=data.get('living_condition_name'),
            planning_name=data.get('planning_name')
        ),
        reply_markup=edit_announcement_kb(),
        parse_mode='HTML'
    )
    await state.set_state(MyAnnouncementEditState.confirm)
    await state.update_data(data)
    print(await state.get_state())
    print(await state.get_data())
    await callback.answer()

def decode_image(file_path, exs):
    with open(str(file_path), 'rb') as image_read:
        encoded_string = base64.b64encode(image_read.read())
    return f"data:image/{exs[1::]};base64,{encoded_string.decode('ascii')}"



@router.message(MyAnnouncementEditState.house_edit, F.text)
async def announcement_create_house(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == MyAnnouncementEditState.house_edit:
        house = message.text
        house_id = await house_validate(house, message.from_user.id)

        if house_id:
            await state.update_data(house=house_id)
            data = await state.update_data(house_name=house)
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
        else:
            await message.answer(_('Оберіть значення з клавіатури. \n'
                                 'Або вірно перепишіть назву будинку :)'))

@router.message(MyAnnouncementEditState.section_edit, F.text)
async def announcement_create_section(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    section = message.text
    house = check_data['house']
    section_id = await section_validate(house, section, message.from_user.id)

    if section_id:
        await state.update_data(section=section_id)
        data = await state.update_data(section_name=section)
        if current_state == MyAnnouncementEditState.section_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_("Оберіть будь-ласка значення з клавіатури. \n"
                                 "Або вірно перепишіть назву секції :)"),
                                 reply_markup=await section_kb(house, message.from_user.id))


@router.message(MyAnnouncementEditState.corps_edit, F.text)
async def announcement_create_corps(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    corps = message.text
    house = check_data['house']
    corps_id = await corps_validate(house, corps, message.from_user.id)

    if corps_id:
        await state.update_data(corps=corps_id)
        data = await state.update_data(corps_name=corps)
        if current_state == MyAnnouncementEditState.corps_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_("Оберіть будь-ласка значення з клавіатури. \n"
                                 "Або вірно перепишіть назву корпус :)"),
                                 reply_markup=await corps_kb(house, message.from_user.id))



@router.message(MyAnnouncementEditState.floor_edit, F.text)
async def announcement_create_floor(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    floor = message.text
    house = check_data['house']
    floor_id = await floor_validate(house, floor, message.from_user.id)

    if floor_id:
        await state.update_data(floor=floor_id)
        data = await state.update_data(floor_name=floor)
        if current_state == MyAnnouncementEditState.floor_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_("Оберіть будь-ласка значення з клавіатури. \n"
                                 "Або вірно перепишіть назву поверху :)"),
                                 reply_markup=await floor_kb(house, message.from_user.id))



@router.message(MyAnnouncementEditState.room_count_edit, F.text)
async def announcement_create_room_count(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    room_count = message.text
    if room_count_validate(room_count):
        data = await state.update_data(room_amount=room_count)
        if current_state == MyAnnouncementEditState.room_count_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )

    else:
        await message.answer(_('Введіть кількість кімнат \n'
                                 'Кімнат може бути від 1 до 7 та бути числом'))

@router.message(MyAnnouncementEditState.price_edit, F.text)
async def announcement_create_price(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    price = message.text

    if price_validate(price):
        data = await state.update_data(price=price)
        if current_state == MyAnnouncementEditState.price_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_('Введіть ціну ще раз \n'
                                 'Діапазон ціни може бути від 10 000 до 100 000 000'))


@router.message(MyAnnouncementEditState.area_edit, F.text)
async def announcement_create_area(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    area = message.text
    if area_validate(area):
        data = await state.update_data(square=area)
        if current_state == MyAnnouncementEditState.area_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_('Введіть площу квартири повторно \n'
                                 'Діапазон площі від 10 до 250 м. кв.'))


@router.message(MyAnnouncementEditState.kitchen_area_edit, F.text)
async def announcement_create_kithcen_area(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    kitchen_area = message.text
    area = check_data.get('square')

    if kitchen_area_validate(area, kitchen_area):
        data = await state.update_data(kitchen_square=kitchen_area)
        if current_state == MyAnnouncementEditState.kitchen_area_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_('Введіть площу кухні повторно \n'
                                 'Діапазон площі від 10 до 250 м. кв \n'
                                 'Кухня не може перевищувати від половини загальної площі'))


@router.message(MyAnnouncementEditState.balcony_edit, F.text)
async def announcement_create_balcony(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    balcony = message.text
    if balcony_validator(balcony):
        if balcony == 'Так':
            await state.update_data(balcony='true')
        elif balcony == 'Ні':
            await state.update_data(balcony='false')
        data = await state.update_data(balcony_name=balcony)
        if current_state == MyAnnouncementEditState.balcony_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_('Я не розумію про що ви...\n'
                                 'Оберіть варіант з кнопки'),
                                 reply_markup=balcony_bool())

@router.message(MyAnnouncementEditState.commission_edit, F.text)
async def announcement_create_commission(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    commission = message.text
    price = check_data.get('price')

    if commission_validate(commission, price):
        data = await state.update_data(commission=commission)
        if current_state == MyAnnouncementEditState.commission_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_('Введіть комісію для агента \n'
                                 'Діапазон комісії від 10 до 30% від повної вартості квартири'))

@router.message(MyAnnouncementEditState.district_edit, F.text)
async def announcement_create_district(message: types.Message, state:FSMContext):
    current_state = await state.get_state()
    district = message.text
    data = await state.update_data(district=district)
    if current_state == MyAnnouncementEditState.district_edit:
        await state.set_state(MyAnnouncementEditState.confirm)
        await message.answer_photo(
            photo=FSInputFile(data.get('general_src')),
            caption=_(
                "Будинок: {house_name}\n"
                "Секція: {section_name}\n"
                "Корпус: {corps_name}\n"
                "Поверх: {floor_name}\n"
                "К-сть кімнат: {room_amount}\n"
                "Ціна: {price}\n"
                "Площа: {square}\n"
                "Площа кухні: {kitchen_square}\n"
                "Балкон: {balcony_name}\n"
                "Вулиця: {district}\n"
                "Район: {micro_district}\n"
                "Стан: {living_condition_name}\n"
                "Планування: {planning_name}\n\n"
                "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
            ).format(
                house_name=data.get('house_name'),
                section_name=data.get('section_name'),
                corps_name=data.get('corps_name'),
                floor_name=data.get('floor_name'),
                room_amount=data.get('room_amount'),
                price=data.get('price'),
                square=data.get('square'),
                kitchen_square=data.get('kitchen_square'),
                balcony_name=data.get('balcony_name'),
                district=data.get('district'),
                micro_district=data.get('micro_district'),
                living_condition_name=data.get('living_condition_name'),
                planning_name=data.get('planning_name')
            ),
            reply_markup=edit_announcement_kb(),
            parse_mode='HTML'
        )

@router.message(MyAnnouncementEditState.micro_district_edit, F.text)
async def announcement_create_micro_district(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    micro_district = message.text
    data = await state.update_data(micro_district=micro_district)
    if current_state == MyAnnouncementEditState.micro_district_edit:
        await state.set_state(MyAnnouncementEditState.confirm)
        await message.answer_photo(
            photo=FSInputFile(data.get('general_src')),
            caption=_(
                "Будинок: {house_name}\n"
                "Секція: {section_name}\n"
                "Корпус: {corps_name}\n"
                "Поверх: {floor_name}\n"
                "К-сть кімнат: {room_amount}\n"
                "Ціна: {price}\n"
                "Площа: {square}\n"
                "Площа кухні: {kitchen_square}\n"
                "Балкон: {balcony_name}\n"
                "Вулиця: {district}\n"
                "Район: {micro_district}\n"
                "Стан: {living_condition_name}\n"
                "Планування: {planning_name}\n\n"
                "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
            ).format(
                house_name=data.get('house_name'),
                section_name=data.get('section_name'),
                corps_name=data.get('corps_name'),
                floor_name=data.get('floor_name'),
                room_amount=data.get('room_amount'),
                price=data.get('price'),
                square=data.get('square'),
                kitchen_square=data.get('kitchen_square'),
                balcony_name=data.get('balcony_name'),
                district=data.get('district'),
                micro_district=data.get('micro_district'),
                living_condition_name=data.get('living_condition_name'),
                planning_name=data.get('planning_name')
            ),
            reply_markup=edit_announcement_kb(),
            parse_mode='HTML'
        )


@router.message(MyAnnouncementEditState.live_condition_edit, F.text)
async def announcement_create_living_condition(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    living_condition = message.text
    if living_condition_validator(living_condition):
        if living_condition == _('Чорнова'):
            await state.update_data(living_condition='draft')
        elif living_condition == _('Потрібен ремонт'):
            await state.update_data(living_condition='repair')
        elif living_condition == _('В жилому стані'):
            await state.update_data(living_condition='good')
        data = await state.update_data(living_condition_name=living_condition)
        if current_state == MyAnnouncementEditState.live_condition_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_('Не відомий для мене стан квартири...\n'
                                 'Оберіть планування з кнопок нижче'),
                                 reply_markup=living_condition_kb())


@router.message(MyAnnouncementEditState.planning_edit, F.text)
async def announcement_create_planning(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    planning = message.text
    if planning_validator(planning):
        if planning == _('Студія-санвузол'):
            await state.update_data(planning='studio-bathroom')
        if planning == _('Студія'):
            await state.update_data(planning='studio')
        data = await state.update_data(planning_name=planning)
        if current_state == MyAnnouncementEditState.planning_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.answer(_('Не відомий для мене планування...\n'
                                 'Оберіть планування з кнопок нижче'),
                                 reply_markup=planning_kb())


@router.message(MyAnnouncementEditState.scheme_edit, F.photo)
async def announcement_create_scheme(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    photo = message.photo[-1]
    if photo_validate(photo):
        file = await bot.get_file(photo.file_id)
        filename, file_extension = os.path.splitext(file.file_path)
        src = 'media/announcement/' + file.file_id + file_extension
        await bot.download_file(file_path=file.file_path, destination=src)
        data = await state.update_data(scheme=decode_image(src, file_extension))
        if current_state == MyAnnouncementEditState.scheme_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
    else:
        await message.delete()
        await message.answer(_('Надішліть фото-схему повторно \n'
                                 'Висота не повина перевищувати 720 px\n'
                                 'Ширина не повинна перевищувати 1280 px\n'
                                 'Максимальний розмір фото 20 mb'))


@router.message(MyAnnouncementEditState.photo_gallery_edit, F.photo)
async def announcement_create_photo_gallery(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    image = message.photo[-1]
    if photo_validate(image):
        file = await bot.get_file(image.file_id)
        filename, file_extension = os.path.splitext(file.file_path)
        src = 'media/announcement/gallery/' + file.file_id + file_extension
        await bot.download_file(file_path=file.file_path, destination=src)
        await state.update_data(general_src=src)
        data = await state.update_data(image=decode_image(src, file_extension))
        if current_state == MyAnnouncementEditState.photo_gallery_edit:
            await state.set_state(MyAnnouncementEditState.confirm)
            await message.answer_photo(
                photo=FSInputFile(data.get('general_src')),
                caption=_(
                    "Будинок: {house_name}\n"
                    "Секція: {section_name}\n"
                    "Корпус: {corps_name}\n"
                    "Поверх: {floor_name}\n"
                    "К-сть кімнат: {room_amount}\n"
                    "Ціна: {price}\n"
                    "Площа: {square}\n"
                    "Площа кухні: {kitchen_square}\n"
                    "Балкон: {balcony_name}\n"
                    "Вулиця: {district}\n"
                    "Район: {micro_district}\n"
                    "Стан: {living_condition_name}\n"
                    "Планування: {planning_name}\n\n"
                    "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                ).format(
                    house_name=data.get('house_name'),
                    section_name=data.get('section_name'),
                    corps_name=data.get('corps_name'),
                    floor_name=data.get('floor_name'),
                    room_amount=data.get('room_amount'),
                    price=data.get('price'),
                    square=data.get('square'),
                    kitchen_square=data.get('kitchen_square'),
                    balcony_name=data.get('balcony_name'),
                    district=data.get('district'),
                    micro_district=data.get('micro_district'),
                    living_condition_name=data.get('living_condition_name'),
                    planning_name=data.get('planning_name')
                ),
                reply_markup=edit_announcement_kb(),
                parse_mode='HTML'
            )
        await message.delete()
        await message.answer(_('Надішліть фото повторно \n'
                                 'Висота не повина перевищувати 720 px\n'
                                 'Ширина не повинна перевищувати 1280 px\n'
                                 'Максимальний розмір фото 20 mb'))

@router.message(MyAnnouncementEditState.location_edit, F.location)
async def announcement_create_location(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    location = message.location
    data = await state.update_data(location=str(location.longitude) + str(location.latitude))
    if current_state == MyAnnouncementEditState.location_edit:
        await state.set_state(MyAnnouncementEditState.confirm)
        await message.answer_photo(
            photo=FSInputFile(data.get('general_src')),
            caption=_(
                "Будинок: {house_name}\n"
                "Секція: {section_name}\n"
                "Корпус: {corps_name}\n"
                "Поверх: {floor_name}\n"
                "К-сть кімнат: {room_amount}\n"
                "Ціна: {price}\n"
                "Площа: {square}\n"
                "Площа кухні: {kitchen_square}\n"
                "Балкон: {balcony_name}\n"
                "Вулиця: {district}\n"
                "Район: {micro_district}\n"
                "Стан: {living_condition_name}\n"
                "Планування: {planning_name}\n\n"
                "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
            ).format(
                house_name=data.get('house_name'),
                section_name=data.get('section_name'),
                corps_name=data.get('corps_name'),
                floor_name=data.get('floor_name'),
                room_amount=data.get('room_amount'),
                price=data.get('price'),
                square=data.get('square'),
                kitchen_square=data.get('kitchen_square'),
                balcony_name=data.get('balcony_name'),
                district=data.get('district'),
                micro_district=data.get('micro_district'),
                living_condition_name=data.get('living_condition_name'),
                planning_name=data.get('planning_name')
            ),
            reply_markup=edit_announcement_kb(),
            parse_mode='HTML'
        )


@router.message(MyAnnouncementEditState.confirm)
async def announcement_create_confirm(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()

    if current_state == MyAnnouncementEditState.confirm:
        if message.text == _('Створити'):
            data = await state.get_data()
            await state.clear()
            await message.answer(_('Чудово. \n'
                                 'Оновлюю квартиру в системі...'),
                                 reply_markup=ReplyKeyboardRemove())
            user = UserAPIClient(message.from_user.id)
            user_id = await user.profile()
            user_data = {
                "house": data.get('house'),
                "section": data.get('section'),
                "floor": data.get('floor'),
                "corps": data.get('corps'),
                "scheme": data.get("scheme"),
                "photo_gallery": [
                    {
                        "image": data.get("scheme")
                    }
                ],
                "room_amount": data.get("room_amount"),
                "price": data.get("price"),
                "square": data.get("square"),
                "kitchen_square": data.get("kitchen_square"),
                "balcony": data.get("balcony"),
                "commission": data.get("commission"),
                "district": data.get("district"),
                "micro_district": data.get("micro_district"),
                "living_condition": data.get("living_condition"),
                "planning": data.get("planning"),
                "user": user_id['id']
            }
            announcement = AnnouncementAPIClient(message.from_user.id)
            create = await announcement.update_announcement_user(user_data=user_data, flat_id=data['id'])
            if create:
                await message.answer_photo(
                    photo=FSInputFile(data.get('general_src')),
                    caption=_(
                        "Будинок: {house_name}\n"
                        "Секція: {section_name}\n"
                        "Корпус: {corps_name}\n"
                        "Поверх: {floor_name}\n"
                        "К-сть кімнат: {room_amount}\n"
                        "Ціна: {price}\n"
                        "Площа: {square}\n"
                        "Площа кухні: {kitchen_square}\n"
                        "Балкон: {balcony_name}\n"
                        "Вулиця: {district}\n"
                        "Район: {micro_district}\n"
                        "Стан: {living_condition_name}\n"
                        "Планування: {planning_name}\n\n"
                        "Перевірте оголошення якщо все вірно натисніть кнопку <b>Створити</b>"
                    ).format(
                        house_name=data.get('house_name'),
                        section_name=data.get('section_name'),
                        corps_name=data.get('corps_name'),
                        floor_name=data.get('floor_name'),
                        room_amount=data.get('room_amount'),
                        price=data.get('price'),
                        square=data.get('square'),
                        kitchen_square=data.get('kitchen_square'),
                        balcony_name=data.get('balcony_name'),
                        district=data.get('district'),
                        micro_district=data.get('micro_district'),
                        living_condition_name=data.get('living_condition_name'),
                        planning_name=data.get('planning_name')
                    ))
                await message.answer(_('оголошення було оновлено'), reply_markup=main_kb())
            else:
                await message.answer(_('Сталась помилка спробуйте ще раз'),
                                     reply_markup=main_kb())
        elif message.text == _('Редагувати будинок'):
            await state.set_state(MyAnnouncementEditState.house_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть будинок: '),
                                 reply_markup=await house_kb(message.from_user.id))
        elif message.text == _('Редагувати секцію'):
            data = await state.get_data()
            await state.set_state(MyAnnouncementEditState.section_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть секцію: '),
                                 reply_markup=await section_kb(data.get('house'), message.from_user.id))
        elif message.text == _('Редагувати корпус'):
            data = await state.get_data()
            await state.set_state(MyAnnouncementEditState.corps_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть корпус: '),
                                 reply_markup=await corps_kb(data.get('house'), message.from_user.id))
        elif message.text == _('Редагувати поверх'):
            data = await state.get_data()
            await state.set_state(MyAnnouncementEditState.floor_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть поверх: '),
                                 reply_markup=await floor_kb(data.get('house'), message.from_user.id))
        elif message.text == _('Редагувати к-сть кімнат'):
            await state.set_state(MyAnnouncementEditState.room_count_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть кількість кімнат: '),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати ціну'):
            await state.set_state(MyAnnouncementEditState.price_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть ціну:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати площу'):
            await state.set_state(MyAnnouncementEditState.area_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть площу:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати площу кухні'):
            await state.set_state(MyAnnouncementEditState.kitchen_area_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть площу кухні:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати балкон'):
            await state.set_state(MyAnnouncementEditState.balcony_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Чи є у вас балкон:'),
                                 reply_markup=balcony_bool())
        elif message.text == _('Редагувати комісію'):
            await state.set_state(MyAnnouncementEditState.commission_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть комісію:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати вулицю'):
            await state.set_state(MyAnnouncementEditState.district_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть вулицю:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати район'):
            await state.set_state(MyAnnouncementEditState.micro_district_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть район:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати стан'):
            await state.set_state(MyAnnouncementEditState.live_condition_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть стан:'),
                                 reply_markup=living_condition_kb())
        elif message.text == _('Редагувати планування'):
            await state.set_state(MyAnnouncementEditState.planning_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть планування:'),
                                 reply_markup=planning_kb())
        elif message.text == _('Редагувати схему'):
            await state.set_state(MyAnnouncementEditState.scheme_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Відправте схему як фото:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати фото'):
            await state.set_state(MyAnnouncementEditState.photo_gallery_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Надішліть фото квартири:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати локацію'):
            await state.set_state(MyAnnouncementEditState.location_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Надішліть локацію через гео телеграму:'),
                                 reply_markup=request_location_kb())
        elif message.text == _('Відмінити'):
            await state.clear()
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Ви повернулися до головного меню'),
                                 reply_markup=main_kb())
        else:
            await message.answer(_('Оберіть дію з клавіатури'),
                                 reply_markup=edit_announcement_kb())




