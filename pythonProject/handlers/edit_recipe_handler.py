from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keybords import choose_edit_field, choose_wich_type_of_correct_to_steps, choose_wich_type_of_correct_to_ingredients, main_menu, choose_position_to_add_ingredient, choose_position_to_add_step
from database import get_values_from_edit_field, update_data, get_recipe, update_new_ingredients, get_ingredients_for_delete, confirm_delete_need_ingredient, \
    delete_need_ingredient, choose_ingredient_to_redact, confirm_ingredient_redact, update_ingredients, \
    confirm_addition_ing, confirm_addition_step, update_new_steps
from states import EditRecipeState
from bot.messages import MAIN_MENU
from utils import confirm_correct_value

edit_recipe_router = Router()

@edit_recipe_router.callback_query(F.data.startswith('correct_'))
async def choose_edit_field_of_dish(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выбери, что будешь редактировать в рецепте.', reply_markup=await choose_edit_field(callback))

@edit_recipe_router.callback_query(F.data.startswith(('edit_name_', 'edit_description_')))
async def edit_choosen_field(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await get_values_from_edit_field(callback, state)

#ToDo новый код
@edit_recipe_router.callback_query(F.data.startswith('edit_ingredients_'))
async def choose_edit_ingredients_action(callback: CallbackQuery):
    await callback.answer()
    recipe_name = callback.data.split('_')[2]
    await callback.message.edit_text('Выбери действие с ингредиентами:', reply_markup=choose_wich_type_of_correct_to_ingredients(recipe_name))

@edit_recipe_router.callback_query(F.data.startswith('edit_steps_'))
async def choose_edit_ingredients_action(callback: CallbackQuery):
    await callback.answer()
    recipe_name = callback.data.split('_')[2]
    await callback.message.edit_text('Выбери действие с шагами приготовления:', reply_markup=choose_wich_type_of_correct_to_steps(recipe_name))

@edit_recipe_router.callback_query(F.data.startswith('add_ingredient_'))
async def choose_position_to_add_ingredient(callback: CallbackQuery):
    await callback.answer()
    recipe = await get_recipe(callback.from_user.id, callback.data.split('_')[2])
    if not recipe:
        await callback.message.answer("Ошибка: рецепт не найден.")
        return

    ingredients = recipe.ingredients.split("\n")
    await callback.message.edit_text(f'Вот текущию список ингредиентов:\n{'\n'.join(ingredients)}\n\nВыберите, куда добавить новый ингредиент:', reply_markup=await choose_position_to_add_ingredient(callback, ingredients))

@edit_recipe_router.callback_query(F.data.startswith('add_step_'))
async def choose_position_to_add_step(callback: CallbackQuery):
    await callback.answer()
    recipe = await get_recipe(callback.from_user.id, callback.data.split('_')[2])
    if not recipe:
        await callback.message.answer("Ошибка: рецепт не найден.")
        return

    steps = recipe.steps.split("\n")
    await callback.message.edit_text(f'Вот текущию список шагов приготовления:\n{'\n'.join(steps)}\n\nВыберите, куда добавить новый ингредиент:', reply_markup=await choose_position_to_add_step(callback, steps))


@edit_recipe_router.callback_query(F.data.startswith('add_pos_ingredient_'))
async def ask_new_ingredient(callback: CallbackQuery, state: FSMContext):
    _, _, _, recipe_name, position = callback.data.split('_')
    await state.update_data(recipe_name=recipe_name, position=int(position))
    await state.set_state(EditRecipeState.add_new_ing)
    await callback.answer()
    await callback.message.edit_text("Введите новый ингредиент:")

@edit_recipe_router.callback_query(F.data.startswith('add_pos_step_'))
async def ask_new_step(callback: CallbackQuery, state: FSMContext):
    _, _, _, recipe_name, position = callback.data.split('_')
    await state.update_data(recipe_name=recipe_name, position=int(position))
    await state.set_state(EditRecipeState.add_new_step)
    await callback.answer()
    await callback.message.edit_text("Введите новый шаг приготовления:")

@edit_recipe_router.message(EditRecipeState.add_new_ing)
async def confirm_ingredient_addition(message: Message, state: FSMContext):
    await confirm_addition_ing(message, state)

@edit_recipe_router.message(EditRecipeState.add_new_step)
async def confirm_step_addition(message: Message, state: FSMContext):
    await confirm_addition_step(message, state)

@edit_recipe_router.callback_query(F.data == "confirm_add_ingredient")
async def save_new_ingredient(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await update_new_ingredients(callback, state)

@edit_recipe_router.callback_query(F.data == "confirm_add_step")
async def save_new_ingredient(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await update_new_steps(callback, state)

@edit_recipe_router.callback_query(F.data == "cancel_add_ingredient")
async def cancel_ingredient_addition(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавление отменено.')
    await callback.message.edit_text(MAIN_MENU,reply_markup=main_menu)
    await state.clear()

@edit_recipe_router.callback_query(F.data == "cancel_add_step")
async def cancel_ingredient_addition(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавление отменено.')
    await callback.message.edit_text(MAIN_MENU,reply_markup=main_menu)
    await state.clear()

@edit_recipe_router.callback_query(F.data.startswith('del_ingredient_'))
async def choose_ingredient_to_delete(callback: CallbackQuery):
    await get_ingredients_for_delete(callback)

@edit_recipe_router.callback_query(F.data.startswith('confirm_del_ingredient_'))
async def confirm_delete_ingredient(callback: CallbackQuery, state: FSMContext):
    await confirm_delete_need_ingredient(callback, state)

@edit_recipe_router.callback_query(F.data == 'cancel_delete_ingredient')
async def cancel_delete_ingredient(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Удаление отменено')
    await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu)
    await state.clear()

@edit_recipe_router.callback_query(F.data == "execute_delete_ingredient")
async def execute_delete_ingredient(callback: CallbackQuery, state: FSMContext):
    await delete_need_ingredient(callback=callback, state=state)

@edit_recipe_router.callback_query(F.data.startswith('update_ingredient_'))
async def choose_ingredient_to_edit(callback: CallbackQuery):
    await choose_ingredient_to_redact(callback)

@edit_recipe_router.callback_query(F.data.startswith('edit_ingredient_'))
async def ask_new_ingredient_value(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    _, _, recipe_name, index = callback.data.split('_')
    index = int(index)

    recipe = await get_recipe(callback.from_user.id, recipe_name)
    ingredients = recipe.ingredients.split('\n')

    await state.update_data(recipe_name=recipe_name, index=index)
    await state.set_state(EditRecipeState.correct_ing)

    await callback.message.edit_text(f"Текущее значение ингредиента: {ingredients[index]}\n\nВведите новое значение для ингредиента:")

@edit_recipe_router.message(EditRecipeState.correct_ing)
async def confirm_ingredient_update(message: Message, state: FSMContext):
    await confirm_ingredient_redact(message, state)

@edit_recipe_router.callback_query(F.data == 'cancle_update')
async def cancle_update_ingredient(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Изменения не сохранены')
    await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu)
    await state.clear()

@edit_recipe_router.callback_query(F.data == "confirm_ingredient_update")
async def update_ingredient_in_db(callback: CallbackQuery, state: FSMContext):
    await update_ingredients(callback, state)


#ToDo Конец нового кода



# @edit_recipe_router.callback_query(F.data.startswith('redact_step_'))
# async def wait_correct_step(callback: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     cur_step = data['steps'][int(callback.data.split('_')[2]) - 1]
#     await state.update_data(cur_step=cur_step)
#     await state.set_state(EditRecipeState.recipe_steps)
#     await callback.answer()
#     await callback.message.edit_text(f'Вот текущий шаг готовки, который вы хотите реадктировать: {cur_step}\n\nВведите новый шаг.')

# @edit_recipe_router.message(EditRecipeState.recipe_ingredients)
# async def get_coorect_ingredient(message: Message, state: FSMContext):
#     await state.update_data(new_ingredient=message.text.capitalize())
#     await confirm_correct_value(message, state)

# @edit_recipe_router.message(EditRecipeState.recipe_steps)
# async def get_correct_step(message: Message, state: FSMContext):
#     await state.update_data(new_step=message.text.capitalize())
#     await confirm_correct_value(message, state)

@edit_recipe_router.message(EditRecipeState.recipe_name)
async def get_correct_recipe_name(message: Message, state: FSMContext):
    await state.update_data(new_recipe_name=message.text.capitalize())
    await confirm_correct_value(message, state)

@edit_recipe_router.message(EditRecipeState.recipe_description)
async def get_correct_recipe_description(message: Message, state: FSMContext):
    await state.update_data(new_description=message.text.capitalize())
    await confirm_correct_value(message, state)

@edit_recipe_router.callback_query(F.data == 'confirm_redact')
async def update_data_in_database(callabck: CallbackQuery, state: FSMContext):
    await update_data(callabck, state)
    await callabck.answer('Данные успешно обновлены')
    await state.clear()
    await callabck.message.edit_text(MAIN_MENU, reply_markup=main_menu)
