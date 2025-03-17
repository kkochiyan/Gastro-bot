from aiogram.fsm.state import StatesGroup,State

class GenerateObject(StatesGroup):
    photo = State()
    name_or_description = State()