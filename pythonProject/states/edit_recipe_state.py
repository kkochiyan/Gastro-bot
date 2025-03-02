from aiogram.fsm.state import StatesGroup,State

class EditRecipeState(StatesGroup):
    waiting_for_new_value = State()
    waiting_for_steps = State()