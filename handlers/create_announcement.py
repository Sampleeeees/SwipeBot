import base64
import json
import os.path
from aiogram.utils.i18n import gettext as _
from keyboards.general.menu import main_kb
from services.api_client import UserAPIClient, AnnouncementAPIClient
from aiogram import Router, F, types, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from states.announ_create import AnnouncementCreateState
from keyboards.general.announcement import (balcony_bool,
                                            living_condition_kb,
                                            planning_kb,
                                            house_kb,
                                            section_kb,
                                            corps_kb,
                                            floor_kb,
                                            request_location_kb,
                                            edit_announcement_kb)
from validators.create_announcement_validator import (balcony_validator,
                                                      living_condition_validator,
                                                      planning_validator,
                                                      house_validate,
                                                      section_validate,
                                                      corps_validate,
                                                      floor_validate,
                                                      room_count_validate,
                                                      price_validate,
                                                      area_validate,
                                                      kitchen_area_validate,
                                                      commission_validate,
                                                      photo_validate)
from aiogram.types import ReplyKeyboardRemove, FSInputFile

router = Router()

def decode_image(file_path, exs):
    with open(str(file_path), 'rb') as image_read:
        encoded_string = base64.b64encode(image_read.read())
    return f"data:image/{exs[1::]};base64,{encoded_string.decode('ascii')}"

@router.message(Text(_('Створити оголошення')))
async def start_create_announcement(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(_('Ви перейшли до створення оголошення'))
    await state.set_state(AnnouncementCreateState.house)
    await message.answer(_('Оберіть будинок в списку нижче:'), reply_markup=await house_kb(message.from_user.id))



@router.message(AnnouncementCreateState.house, F.text)
@router.message(AnnouncementCreateState.house_edit, F.text)
async def announcement_create_house(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AnnouncementCreateState.house:
        house = message.text
        house_id = await house_validate(house, message.from_user.id)

        if house_id:
            print("House ID:", house_id)
            await state.update_data(house=house_id)
            await state.update_data(house_name=house)
            await state.set_state(AnnouncementCreateState.section)
            await message.answer(_('Тепер оберіть секцію будинку'),
                                 reply_markup=await section_kb(house_id, user_id=message.from_user.id))
        else:
            await message.answer(_("Оберіть будь-ласка значення з клавіатури. \n"
                                 "Або вірно перепишіть назву будинку :)"),
                                 reply_markup=await house_kb(message.from_user.id))
    elif current_state == AnnouncementCreateState.house_edit:
        house = message.text
        house_id = await house_validate(house, message.from_user.id)

        if house_id:
            await state.update_data(house=house_id)
            data = await state.update_data(house_name=house)
            await state.set_state(AnnouncementCreateState.confirm)
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

@router.message(AnnouncementCreateState.section, F.text)
@router.message(AnnouncementCreateState.section_edit, F.text)
async def announcement_create_section(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    section = message.text
    house = check_data['house']
    section_id = await section_validate(house, section, message.from_user.id)

    if section_id:
        await state.update_data(section=section_id)
        data = await state.update_data(section_name=section)
        if current_state == AnnouncementCreateState.section:
            await state.set_state(AnnouncementCreateState.corps)
            await message.answer(_('Оберіть корпус'), reply_markup=await corps_kb(house, message.from_user.id))

        elif current_state == AnnouncementCreateState.section_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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


@router.message(AnnouncementCreateState.corps, F.text)
@router.message(AnnouncementCreateState.corps_edit, F.text)
async def announcement_create_corps(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    corps = message.text
    house = check_data['house']
    corps_id = await corps_validate(house, corps, message.from_user.id)

    if corps_id:
        await state.update_data(corps=corps_id)
        data = await state.update_data(corps_name=corps)
        if current_state == AnnouncementCreateState.corps:
            await state.set_state(AnnouncementCreateState.floor)
            await message.answer(_('Оберіть поверх'), reply_markup=await floor_kb(house, message.from_user.id))

        elif current_state == AnnouncementCreateState.corps_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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
                                 "Або вірно перепишіть назву корпусу :)"),
                                 reply_markup=await corps_kb(house, message.from_user.id))


@router.message(AnnouncementCreateState.floor, F.text)
@router.message(AnnouncementCreateState.floor_edit, F.text)
async def announcement_create_floor(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    floor = message.text
    house = check_data['house']
    floor_id = await floor_validate(house, floor, message.from_user.id)

    if floor_id:
        await state.update_data(floor=floor_id)
        data = await state.update_data(floor_name=floor)
        if current_state == AnnouncementCreateState.floor:
            await state.set_state(AnnouncementCreateState.room_count)
            await message.answer(_('Введіть кількість кімнат:'), reply_markup=ReplyKeyboardRemove())

        elif current_state == AnnouncementCreateState.floor_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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



@router.message(AnnouncementCreateState.room_count, F.text)
@router.message(AnnouncementCreateState.room_count_edit, F.text)
async def announcement_create_room_count(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    room_count = message.text
    if room_count_validate(room_count):
        data = await state.update_data(room_amount=room_count)
        if current_state == AnnouncementCreateState.room_count:
            await state.set_state(AnnouncementCreateState.price)
            await message.answer(_('Введіть ціну квартири: '))
        elif current_state == AnnouncementCreateState.room_count_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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

@router.message(AnnouncementCreateState.price, F.text)
@router.message(AnnouncementCreateState.price_edit, F.text)
async def announcement_create_price(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    price = message.text

    if price_validate(price):
        data = await state.update_data(price=price)
        if current_state == AnnouncementCreateState.price:
            await state.set_state(AnnouncementCreateState.area)
            await message.answer(_('Введіть загальну площу квартири:'))
        elif current_state == AnnouncementCreateState.price_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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


@router.message(AnnouncementCreateState.area, F.text)
@router.message(AnnouncementCreateState.area_edit, F.text)
async def announcement_create_area(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    area = message.text
    if area_validate(area):
        data = await state.update_data(square=area)
        if current_state == AnnouncementCreateState.area:
            await state.set_state(AnnouncementCreateState.kitchen_area)
            await message.answer(_('Введіть площу кухні:'))
        elif current_state == AnnouncementCreateState.area_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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


@router.message(AnnouncementCreateState.kitchen_area, F.text)
@router.message(AnnouncementCreateState.kitchen_area_edit, F.text)
async def announcement_create_kithcen_area(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    kitchen_area = message.text
    area = check_data.get('square')

    if kitchen_area_validate(area, kitchen_area):
        data = await state.update_data(kitchen_square=kitchen_area)
        if current_state == AnnouncementCreateState.kitchen_area:
            await state.set_state(AnnouncementCreateState.balcony)
            await message.answer(_('У вас є балкон:'), reply_markup=balcony_bool())
        elif current_state == AnnouncementCreateState.kitchen_area_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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


@router.message(AnnouncementCreateState.balcony, F.text)
@router.message(AnnouncementCreateState.balcony_edit, F.text)
async def announcement_create_balcony(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    balcony = message.text
    if balcony_validator(balcony):
        if balcony == _('Так'):
            await state.update_data(balcony='true')
        elif balcony == _('Ні'):
            await state.update_data(balcony='false')
        data = await state.update_data(balcony_name=balcony)
        if current_state == AnnouncementCreateState.balcony:
            await state.set_state(AnnouncementCreateState.commission)
            await message.answer(_('Введіть комісію агенту:'),reply_markup=ReplyKeyboardRemove())
        elif current_state == AnnouncementCreateState.balcony_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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

@router.message(AnnouncementCreateState.commission, F.text)
@router.message(AnnouncementCreateState.commission_edit, F.text)
async def announcement_create_commission(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    check_data = await state.get_data()
    commission = message.text
    price = check_data.get('price')

    if commission_validate(commission, price):
        data = await state.update_data(commission=commission)
        if current_state == AnnouncementCreateState.commission:
            await state.set_state(AnnouncementCreateState.district)
            await message.answer(_('Введіть вулицю: '))
        elif current_state == AnnouncementCreateState.commission_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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

@router.message(AnnouncementCreateState.district, F.text)
@router.message(AnnouncementCreateState.district_edit, F.text)
async def announcement_create_district(message: types.Message, state:FSMContext):
    current_state = await state.get_state()
    district = message.text
    data = await state.update_data(district=district)
    if current_state == AnnouncementCreateState.district:
        await state.set_state(AnnouncementCreateState.micro_district)
        await message.answer(_('Введіть район:'))
    elif current_state == AnnouncementCreateState.district_edit:
        await state.set_state(AnnouncementCreateState.confirm)
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

@router.message(AnnouncementCreateState.micro_district, F.text)
@router.message(AnnouncementCreateState.micro_district_edit, F.text)
async def announcement_create_micro_district(message: types.Message, state:FSMContext):
    current_state = await state.get_state()
    micro_district = message.text
    data = await state.update_data(micro_district=micro_district)
    if current_state == AnnouncementCreateState.micro_district:
        await state.set_state(AnnouncementCreateState.live_condition)
        await message.answer(_('Оберіть стан:'), reply_markup=living_condition_kb())
    elif current_state == AnnouncementCreateState.micro_district_edit:
        await state.set_state(AnnouncementCreateState.confirm)
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


@router.message(AnnouncementCreateState.live_condition, F.text)
@router.message(AnnouncementCreateState.live_condition_edit, F.text)
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
        if current_state == AnnouncementCreateState.live_condition:
            await state.set_state(AnnouncementCreateState.planning)
            await message.answer(_('Тепер оберіть планування квартири'), reply_markup=planning_kb())
        elif current_state == AnnouncementCreateState.live_condition_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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

@router.message(AnnouncementCreateState.planning, F.text)
@router.message(AnnouncementCreateState.planning_edit, F.text)
async def announcement_create_planning(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    planning = message.text
    if planning_validator(planning):
        if planning == _('Студія-санвузол'):
            await state.update_data(planning='studio-bathroom')
        if planning == _('Студія'):
            await state.update_data(planning='studio')
        data = await state.update_data(planning_name=planning)
        if current_state == AnnouncementCreateState.planning:
            await state.set_state(AnnouncementCreateState.scheme)
            await message.answer('Тепер надішліть схему квартири як фото', reply_markup=ReplyKeyboardRemove())
        elif current_state == AnnouncementCreateState.planning_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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


@router.message(AnnouncementCreateState.scheme, F.photo)
@router.message(AnnouncementCreateState.scheme_edit, F.photo)
async def announcement_create_scheme(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    photo = message.photo[-1]
    if photo_validate(photo):
        file = await bot.get_file(photo.file_id)
        filename, file_extension = os.path.splitext(file.file_path)
        src = 'media/announcement/' + file.file_id + file_extension
        await bot.download_file(file_path=file.file_path, destination=src)
        data = await state.update_data(scheme=decode_image(src, file_extension))
        if current_state == AnnouncementCreateState.scheme:
            image_answer = FSInputFile(src)

            await state.set_state(AnnouncementCreateState.photo_gallery)
            await message.answer_photo(photo=image_answer)
            await message.answer(_('А тепер додайте зображення квартири:'))
        elif current_state == AnnouncementCreateState.scheme_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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

@router.message(AnnouncementCreateState.photo_gallery, F.photo)
@router.message(AnnouncementCreateState.photo_gallery_edit, F.photo)
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
        if current_state == AnnouncementCreateState.photo_gallery:
            image_answer = FSInputFile(src)
            await state.set_state(AnnouncementCreateState.location)
            await message.answer_photo(photo=image_answer)
            await message.answer(_('А тепер передайте геолокацію за допомогою телеграму:'),
                                 reply_markup=request_location_kb())
        elif current_state == AnnouncementCreateState.photo_gallery_edit:
            await state.set_state(AnnouncementCreateState.confirm)
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
        await message.answer(_('Надішліть фото повторно \n'
                                 'Висота не повина перевищувати 720 px\n'
                                 'Ширина не повинна перевищувати 1280 px\n'
                                 'Максимальний розмір фото 20 mb'))

@router.message(AnnouncementCreateState.location, F.location)
@router.message(AnnouncementCreateState.location_edit, F.location)
async def announcement_create_location(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    location = message.location
    data = await state.update_data(location=str(location.longitude) + str(location.latitude))
    if current_state == AnnouncementCreateState.location:
        await state.set_state(AnnouncementCreateState.confirm)
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
    elif current_state == AnnouncementCreateState.location_edit:
        await state.set_state(AnnouncementCreateState.confirm)
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


@router.message(AnnouncementCreateState.confirm)
async def announcement_create_confirm(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()

    if current_state == AnnouncementCreateState.confirm:
        if message.text == _('Створити'):
            data = await state.get_data()
            await state.clear()
            await message.answer(_('Чудово. \n'
                                 'Створюю квартиру в системі...'),
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
                        "image": data.get("image")
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
            create = await announcement.create_announcement_user(user_data=user_data)
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
                ))
                await message.answer(_('оголошення було створено'), reply_markup=main_kb())
            else:
                await message.answer(_('Сталась помилка спробуйте ще раз'),
                                     reply_markup=main_kb())
        elif message.text == _('Редагувати будинок'):
            await state.set_state(AnnouncementCreateState.house_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть будинок: '),
                                 reply_markup=await house_kb(message.from_user.id))
        elif message.text == _('Редагувати секцію'):
            data = await state.get_data()
            await state.set_state(AnnouncementCreateState.section_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть секцію: '),
                                 reply_markup=await section_kb(data.get('house'), message.from_user.id))
        elif message.text == _('Редагувати корпус'):
            data = await state.get_data()
            await state.set_state(AnnouncementCreateState.corps_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть корпус: '),
                                 reply_markup=await corps_kb(data.get('house'), message.from_user.id))
        elif message.text == _('Редагувати поверх'):
            data = await state.get_data()
            await state.set_state(AnnouncementCreateState.floor_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть поверх: '),
                                 reply_markup=await floor_kb(data.get('house'), message.from_user.id))
        elif message.text == _('Редагувати к-сть кімнат'):
            await state.set_state(AnnouncementCreateState.room_count_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть кількість кімнат: '),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати ціну'):
            await state.set_state(AnnouncementCreateState.price_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть ціну:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати площу'):
            await state.set_state(AnnouncementCreateState.area_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть площу:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати площу кухні'):
            await state.set_state(AnnouncementCreateState.kitchen_area_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть площу кухні:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати балкон'):
            await state.set_state(AnnouncementCreateState.balcony_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Чи є у вас балкон:'),
                                 reply_markup=balcony_bool())
        elif message.text == _('Редагувати комісію'):
            await state.set_state(AnnouncementCreateState.commission_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть комісію:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати вулицю'):
            await state.set_state(AnnouncementCreateState.district_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть вулицю:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати район'):
            await state.set_state(AnnouncementCreateState.micro_district_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Введіть район:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати стан'):
            await state.set_state(AnnouncementCreateState.live_condition_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть стан:'),
                                 reply_markup=living_condition_kb())
        elif message.text == _('Редагувати планування'):
            await state.set_state(AnnouncementCreateState.planning_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Оберіть планування:'),
                                 reply_markup=planning_kb())
        elif message.text == _('Редагувати схему'):
            await state.set_state(AnnouncementCreateState.scheme_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Відправте схему як фото:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати фото'):
            await state.set_state(AnnouncementCreateState.photo_gallery_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Надішліть фото квартири:'),
                                 reply_markup=ReplyKeyboardRemove())
        elif message.text == _('Редагувати локацію'):
            await state.set_state(AnnouncementCreateState.location_edit)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Надішліть локацію через гео телеграму:'),
                                 reply_markup=request_location_kb())
        elif message.text == _('Відмінити'):
            await state.clear()
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
            await message.answer(_('Ви повернулися до профілю'),
                                 reply_markup=main_kb())
        else:
            await message.answer(_('Оберіть дію з клавіатури'),
                                 reply_markup=edit_announcement_kb())









