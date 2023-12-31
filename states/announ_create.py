from aiogram.fsm.state import State, StatesGroup

class AnnouncementCreateState(StatesGroup):
    house = State()
    section = State()
    corps = State()
    floor = State()
    room_count = State()
    price = State()
    area = State()
    kitchen_area = State()
    balcony = State()
    commission = State()
    district = State()
    micro_district = State()
    live_condition = State()
    planning = State()
    scheme = State()
    photo_gallery = State()
    location = State()
    house_edit = State()
    section_edit = State()
    corps_edit = State()
    floor_edit = State()
    room_count_edit = State()
    price_edit = State()
    area_edit = State()
    kitchen_area_edit = State()
    balcony_edit = State()
    commission_edit = State()
    district_edit = State()
    micro_district_edit = State()
    live_condition_edit = State()
    planning_edit = State()
    scheme_edit = State()
    photo_gallery_edit = State()
    location_edit = State()
    confirm = State()
