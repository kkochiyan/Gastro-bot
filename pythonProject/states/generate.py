from aiogram.fsm.state import StatesGroup,State

class Generate(StatesGroup):
    text = State()