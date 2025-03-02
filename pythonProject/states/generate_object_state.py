from aiogram.fsm.state import StatesGroup,State

class GenerateObject(StatesGroup):
    photo = State()
    name = State()
    description = State()