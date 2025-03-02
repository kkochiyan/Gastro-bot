from aiogram.fsm.state import StatesGroup,State

class AddRecipe(StatesGroup):
    category = State()
    name = State()
    description = State()
    ingredients = State()
    steps = State()