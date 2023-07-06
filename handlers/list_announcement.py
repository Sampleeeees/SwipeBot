from aiogram import types, Router, F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import URLInputFile, ReplyKeyboardRemove

from database.database import is_authenticated
from keyboards.general.login_and_registration import login_register_kb
from keyboards.general.menu import main_kb
from services.api_client import AnnouncementAPIClient
from handlers.announcement_detail import get_full_flat_data, DEFAULT_IMAGE
from keyboards.inline.announcement import inline_announcement_kb, AnnouncementCallback
from aiogram.utils.i18n import gettext as _

from states.login_state import LoginState

router = Router()

def get_image_ads(url=None):
    """
    return default image if url is None
    """
    image = URLInputFile(
        DEFAULT_IMAGE,
        filename="image")
    if url:
        image.url = url
    return image


def get_image(path=None):
    """
    return default image if path is None
    """
    image = URLInputFile(
        DEFAULT_IMAGE,
        filename="image")
    if path:
        image.url = str(path)
    return image

# endregion image


# region feed
class NegativeIndexError(Exception):
    pass




class AnnouncementStates(StatesGroup):
    announ = State()


user_data = {}

@router.message(Text(_('Оголошення')))
async def announcement_feed(message: types.Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    user = AnnouncementAPIClient(user_id)
    user_data[user_id] = 0
    if is_authenticated(user_id):
        await message.answer(
            _('Вітаю в списку оголошень'),
            reply_markup=main_kb()
        )
        data = await user.list_all_announcement()
        print('Spisok', data)
        if data:
            announ = data[user_data[user_id]]
            print('Detail_data', announ)
            if user_data[user_id] < 0:
                raise NegativeIndexError
            if announ:
                flat_id = announ['flat']['id']
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

                caption_text = _('Будинок: {house} \n'
                                 'Секція: {section}\n'
                                 'Поверх: {floor}\n'
                                 'Корпус: {corps}\n'
                                 'К-сть кімнат: {room_amount}\n'
                                 'Ціна: {price}\n'
                                 'Площа: {square}\n'
                                 'Площа кухні: {kitchen_square}\n'
                                 'Балкон: {balcony}\n'
                                 'Комісія: {commission}\n'
                                 'Вулиця: {district}\n'
                                 'Район: {micro_district}\n'
                                 'Стан: {living_condition}\n'
                                 'Планування: {planning}\n').format(
                    house=house,
                    section=section['name'],
                    floor=floor['name'],
                    corps=corps['name'],
                    room_amount=flat['room_amount'],
                    price=flat['price'],
                    square=flat['square'],
                    kitchen_square=flat['kitchen_square'],
                    balcony=flat['balcony'],
                    commission=flat['commission'],
                    district=flat['district'],
                    micro_district=flat['micro_district'],
                    living_condition=flat['living_condition'],
                    planning=flat['planning']
                )

                media = types.InputMediaPhoto(media=get_image(path=flat["scheme"]),
                                                  caption=caption_text)
                await message.answer_photo(photo=get_image(path=flat['scheme']),
                                           caption=caption_text,
                                            reply_markup=inline_announcement_kb(user_data[user_id]))
        else:
            await message.answer(
                _('Стрічка пуста')
            )
    else:
        await message.answer(
            _('Увійдіть або зареєструйтесь'),
            reply_markup=login_register_kb())
        await state.clear()


@router.callback_query(AnnouncementCallback.filter(F.step.startswith('go_')))
async def announcement_step(callback: types.CallbackQuery, callback_data: AnnouncementCallback):
    user_id = callback.from_user.id
    user = AnnouncementAPIClient(user_id)
    announce = AnnouncementAPIClient(user_id)
    data = await announce.list_all_announcement()
    try:
        if callback_data.step == 'go_next':
            user_data[user_id] += 1
        elif callback_data.step == 'go_previous':
            user_data[user_id] -= 1
        if data:
            announ = data[user_data[user_id]]
            print('Detail_data', announ)
            try:
                if user_data[user_id] < 0:
                    raise NegativeIndexError
                if announ:
                    flat_id = announ['flat']['id']
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

                    caption_text = _('Будинок: {house} \n'
                                     'Секція: {section}\n'
                                     'Поверх: {floor}\n'
                                     'Корпус: {corps}\n'
                                     'К-сть кімнат: {room_amount}\n'
                                     'Ціна: {price}\n'
                                     'Площа: {square}\n'
                                     'Площа кухні: {kitchen_square}\n'
                                     'Балкон: {balcony}\n'
                                     'Комісія: {commission}\n'
                                     'Вулиця: {district}\n'
                                     'Район: {micro_district}\n'
                                     'Стан: {living_condition}\n'
                                     'Планування: {planning}\n').format(
                        house=house,
                        section=section['name'],
                        floor=floor['name'],
                        corps=corps['name'],
                        room_amount=flat['room_amount'],
                        price=flat['price'],
                        square=flat['square'],
                        kitchen_square=flat['kitchen_square'],
                        balcony=flat['balcony'],
                        commission=flat['commission'],
                        district=flat['district'],
                        micro_district=flat['micro_district'],
                        living_condition=flat['living_condition'],
                        planning=flat['planning']
                    )

                    media = types.InputMediaPhoto(media=get_image(path=flat["scheme"]),
                                                  caption=caption_text)
                    await callback.message.edit_media(media=media,
                                                      reply_markup=inline_announcement_kb(user_data[user_id]))
                    await callback.answer(_('Змінено'))

                else:
                    await callback.answer('Check',
                        reply_markup=inline_announcement_kb(user_data[user_id]))
            except IndexError:
                await callback.answer(
                   _('Це було останнє оголошення')
                )
                user_data[user_id] -= 1
            except NegativeIndexError:
                await callback.answer(
                    _('Це перше оголошення')
                )
                user_data[user_id] += 1
    except KeyError:
        await callback.message.answer(
            _('Сталась помилка, перезапустіться командою\n'
              '/start'),
            reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.callback_query(AnnouncementCallback.filter(F.step == "geo"))
async def get_announcement_geolocation(callback: types.CallbackQuery):
    await callback.message.answer_location(
        latitude=46.468851871374525, longitude=30.710127484338713
    )
    await callback.answer()