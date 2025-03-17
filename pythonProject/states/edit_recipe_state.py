from aiogram.fsm.state import StatesGroup,State

class EditRecipeState(StatesGroup):
    recipe_name = State()
    recipe_description = State()
    add_new_ing = State()
    correct_ing = State()
    add_new_step = State()
    correct_step = State()