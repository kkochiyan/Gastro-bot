from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.messages import CATEGORY_OF_SAVED_RECIPES, MAIN_MENU
from keybords import categories_of_saved_recipes, saved_names_recipes_in_need_category, recipe_actions, \
    choose_edit_field, main_menu, confirm_delete_recipe_keyboard, choose_wich_type_of_correct_to_ingredients, \
    choose_wich_type_of_correct_to_steps
from utils import category_defenition, make_card_of_dish_by_data_from_database, send_cooking_steps, confirm_correct_value
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
    await callback.message.edit_text(card_text, reply_markup=await recipe_actions(rows[0].category_name, rows[0].name, rows[0].id))

@show_saved_recipes_router.callback_query(F.data.startswith('delete_'))
async def confirm_delete_recipe(callback: CallbackQuery):
    await callback.answer()
    _, name, recipe_id = callback.data.split('_')
    await callback.message.edit_text(f'Точно хотите удалить рецепт {name}?', reply_markup=confirm_delete_recipe_keyboard(name, recipe_id))

@show_saved_recipes_router.callback_query(F.data.startswith('confirm_delete_'))
async def delete_recipe(callback: CallbackQuery):
    await delete_need_recipe(callback)
    await callback.answer(f'Рецепт {callback.data.split('_')[2]} успешно удален!')
    await callback.message.edit_text(CATEGORY_OF_SAVED_RECIPES, reply_markup=categories_of_saved_recipes)

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

