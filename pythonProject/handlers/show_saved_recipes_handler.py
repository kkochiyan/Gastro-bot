from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.messages import CATEGORY_OF_SAVED_RECIPES, MAIN_MENU
from keybords import categories_of_saved_recipes, saved_names_recipes_in_need_category, recipe_actions, choose_edit_field, main_menu, confirm_delete_recipe_keyboard
from utils import category_defenition, make_card_of_dish_by_data_from_database, recive_steps, send_cooking_steps, confirm_correct_value
from database import get_data_for_card_of_dish, delete_need_recipe, get_data_for_cook, get_values_from_edit_field, update_data
from states import EditRecipeState

show_saved_recipes_router = Router()

@show_saved_recipes_router.callback_query(F.data == 'saved_recipes')
async def choose_category_of_dish(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(CATEGORY_OF_SAVED_RECIPES, reply_markup=categories_of_saved_recipes)

@show_saved_recipes_router.callback_query(F.data.startswith('dish_'))
async def show_recipes_from_need_category(callback: CallbackQuery):
    await callback.answer()
    category = category_defenition(callback.data.split('_')[1])
    await saved_names_recipes_in_need_category(callback=callback, category=category)

@show_saved_recipes_router.callback_query(F.data.startswith('recipe_'))
async def get_card_of_dish(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    rows = await get_data_for_card_of_dish(callback)
    card_text = make_card_of_dish_by_data_from_database(rows)
    await callback.message.edit_text(card_text, reply_markup=await recipe_actions(rows[0].category_name, rows[0].name))

@show_saved_recipes_router.callback_query(F.data.startswith('delete_'))
async def confirm_delete_recipe(callback: CallbackQuery):
    await callback.answer()
    name = callback.data.split('_')[1]
    await callback.message.edit_text(f'Точно хотите удалить рецепт {name}?', reply_markup=confirm_delete_recipe_keyboard(name))

@show_saved_recipes_router.callback_query(F.data.startswith('confirm_delete_'))
async def delete_recipe(callback: CallbackQuery):
    await delete_need_recipe(callback)
    await callback.answer(f'Рецепт {callback.data.split('_')[2]} успешно удален!')
    await callback.message.edit_text(CATEGORY_OF_SAVED_RECIPES, reply_markup=categories_of_saved_recipes)

@show_saved_recipes_router.callback_query(F.data.startswith('correct_'))
async def choose_edit_field_of_dish(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выбери, что будешь редактировать в рецепте.', reply_markup=await choose_edit_field(callback))

@show_saved_recipes_router.callback_query(F.data.startswith('edit_'))
async def edit_choosen_field(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await get_values_from_edit_field(callback, state)

@show_saved_recipes_router.callback_query(F.data.startswith('start_'))
async def start_cook(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await get_data_for_cook(callback, state)
    await send_cooking_steps(callback.message, state)

@show_saved_recipes_router.callback_query(F.data == 'next_step')
async def next_step(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_step = data.get('step_index')
    await state.update_data(step_index=current_step+1)

    await callback.answer()
    await send_cooking_steps(callback.message, state)

@show_saved_recipes_router.callback_query(F.data == 'prev_step')
async def prev_step(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_step = data.get('step_index')
    await state.update_data(step_index=current_step - 1)

    await callback.answer()
    await send_cooking_steps(callback.message, state)

@show_saved_recipes_router.callback_query(F.data == 'finish_cook')
async def finish_cook(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(f"Готовка завершена!\n\n{MAIN_MENU}", reply_markup=main_menu)

@show_saved_recipes_router.callback_query(F.data.startswith('redact_ingredient_'))
async def wait_correct_ingredient(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur_ingredient = data['ingredients'][int(callback.data.split('_')[2]) - 1]
    await state.update_data(cur_ingredient=cur_ingredient)
    await state.set_state(EditRecipeState.recipe_ingredients)
    await callback.answer()
    await callback.message.edit_text(f'Вот текущий ингредиент, который вы хотите редактировать: {cur_ingredient}\n\nВведите новый ингредиент.')

@show_saved_recipes_router.callback_query(F.data.startswith('redact_step_'))
async def wait_correct_step(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cur_step = data['steps'][int(callback.data.split('_')[2]) - 1]
    await state.update_data(cur_step=cur_step)
    await state.set_state(EditRecipeState.recipe_steps)
    await callback.answer()
    await callback.message.edit_text(f'Вот текущий шаг готовки, который вы хотите реадктировать: {cur_step}\n\nВведите новый шаг.')

@show_saved_recipes_router.message(EditRecipeState.recipe_ingredients)
async def get_coorect_ingredient(message: Message, state: FSMContext):
    await state.update_data(new_ingredient=message.text.capitalize())
    await confirm_correct_value(message, state)

@show_saved_recipes_router.message(EditRecipeState.recipe_steps)
async def get_correct_step(message: Message, state: FSMContext):
    await state.update_data(new_step=message.text.capitalize())
    await confirm_correct_value(message, state)

@show_saved_recipes_router.message(EditRecipeState.recipe_name)
async def get_correct_recipe_name(message: Message, state: FSMContext):
    await state.update_data(new_recipe_name=message.text.capitalize())
    await confirm_correct_value(message, state)

@show_saved_recipes_router.message(EditRecipeState.recipe_description)
async def get_correct_recipe_description(message: Message, state: FSMContext):
    await state.update_data(new_description=message.text.capitalize())
    await confirm_correct_value(message, state)

@show_saved_recipes_router.callback_query(F.data == 'confirm_redact')
async def update_data_in_database(callabck: CallbackQuery, state: FSMContext):
    await update_data(callabck, state)
    await callabck.answer('Данные успешно обновлены')
    await state.clear()
    await callabck.message.edit_text(MAIN_MENU, reply_markup=main_menu)
