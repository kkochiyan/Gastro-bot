from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.messages import CATEGORY_OF_SAVED_RECIPES, SAVED_RECIPES_IN_NEED_CATEGORY, MAIN_MENU
from keybords import categories_of_saved_recipes, saved_names_recipes, recipe_actions, choose_edit_field, main_menu
from utils import category_defenition, make_card_of_dish, choose_and_start_edit, recive_steps, send_cooking_steps
from database import get_names_recipes, get_data_for_card_of_dish, delete_need_recipe, update_data_values, update_data_steps, get_data_for_cook
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

    if len(await get_names_recipes(callback, category)) == 0:
        await callback.message.edit_text(f"В категории {category} у вас нет сохраненных рецептов.\n{CATEGORY_OF_SAVED_RECIPES}",
                                         reply_markup=categories_of_saved_recipes)
    else:
        await callback.message.edit_text(SAVED_RECIPES_IN_NEED_CATEGORY, reply_markup=await saved_names_recipes(callback, category))

@show_saved_recipes_router.callback_query(F.data.startswith('recipe_'))
async def get_card_of_dish(callback: CallbackQuery):
    await callback.answer()
    rows = await get_data_for_card_of_dish(callback)
    card_text = make_card_of_dish(rows)
    await callback.message.edit_text(card_text, reply_markup=await recipe_actions(rows[0].category_name, rows[0].name))

@show_saved_recipes_router.callback_query(F.data.startswith('delete_'))
async def delete_recipe(callback: CallbackQuery):
    await callback.answer()
    await delete_need_recipe(callback)
    await callback.message.answer(CATEGORY_OF_SAVED_RECIPES, reply_markup=categories_of_saved_recipes)

@show_saved_recipes_router.callback_query(F.data.startswith('correct_'))
async def choose_edit_field_of_dish(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выбери, что будешь редактировать в рецепте.', reply_markup=await choose_edit_field(callback))

@show_saved_recipes_router.callback_query(F.data.startswith('edit_'))
async def edit_choosen_field(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await choose_and_start_edit(callback, state)

@show_saved_recipes_router.message(EditRecipeState.waiting_for_new_value)
async def saved_edit_values(message: Message, state: FSMContext):
    await update_data_values(message, state)
    await message.answer(MAIN_MENU, reply_markup=main_menu)

@show_saved_recipes_router.message(EditRecipeState.waiting_for_steps)
async def input_edit_steps(message: Message, state: FSMContext):
    await recive_steps(message, state)

@show_saved_recipes_router.callback_query(F.data == 'finish_edit_steps')
async def saved_edit_steps(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await update_data_steps(callback, state)
    await callback.message.answer(MAIN_MENU, reply_markup=main_menu)

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
    await callback.answer()
    await callback.message.edit_text(f"Готовка завершена!\n\n{MAIN_MENU}", reply_markup=main_menu)