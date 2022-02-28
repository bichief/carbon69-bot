from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    get_date = State()
    get_amount = State()
    get_text = State()
    get_id = State()
    get_people = State()
    get_mailing = State()