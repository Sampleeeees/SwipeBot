from aiogram import F, Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from states.profile_state import AnnouncementState
from services.api_client import AnnouncementAPIClient
from keyboards.inline.announcement import inline_announcement_kb

router = Router()

user_data = {}

@router.message(Text('Мої оголошення'))
async def cmd_list_announcement(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = AnnouncementAPIClient(user_id)
    await state.set_state(AnnouncementState.announ)
    list_announce = await user.list_announcement()
    user_data[message.from_user.id] = 0
    if list_announce:
        print(list_announce)
        announ = list_announce[user_data[message.from_user.id]]
        flat_id = announ['flat']
        flat = await user.get_flat(flat_id)
        house_id = flat['house']
        house = await user.get_house(house_id)
        section_id = flat['section']
        floor_id = flat['floor']
        corps_id = flat['corps']
        section = await user.get_section(section_id)
        floor = await user.get_floor(floor_id)
        corps = await user.get_corps(corps_id)
        print(flat)
        print(house)
        await message.answer(f'Будинок: {house} \n'
                             f'Секція: {section["name"]}\n'
                             f'Поверх: {floor["name"]}\n'
                             f'Корпус: {corps["name"]}\n'
                             f'К-сть кімнат: {flat["room_amount"]}\n'
                             f'Ціна: {flat["price"]}\n'
                             f'Площа: {flat["square"]}\n'
                             f'Площа кухні: {flat["kitchen_square"]}\n'
                             f'Балкон: {flat["balcony"]}\n'
                             f'Комісія: {flat["commission"]}\n'
                             f'Вулиця: {flat["district"]}\n'
                             f'Район: {flat["micro_district"]}\n'
                             f'Стан: {flat["living_condition"]}\n'
                             f'Планування: {flat["planning"]}\n',
                             reply_markup=inline_announcement_kb(int(user_id)))
    else:
        await message.answer(f'У вас немає жодного створеного оголошення')