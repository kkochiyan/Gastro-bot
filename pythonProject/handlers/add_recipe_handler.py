from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states import AddRecipe as ar
from bot.messages import ADD_NAME, ADD_DESCRIPTION, ADD_INGREDIENTS, ADD_STEPS, CHOOSE_CATEGORY, MAIN_MENU, ERROR_SMALL_COUNT_OF_SYMBOLS_STEPS
from keybords import categories, main_menu
from utils import category_defenition, make_card_of_dish_by_data_from_user
from database import add_recipe_to_database

add_recipe_router = Router()

@add_recipe_router.callback_query(F.data == 'add_recipe')
async def get_dish_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(CHOOSE_CATEGORY, reply_markup=categories)
    await state.set_state(ar.category)

@add_recipe_router.callback_query(F.data.startswith('category_'))
async def get_dish_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=category_defenition(callback.data.split('_')[1]))
    await state.set_state(ar.name)
    await callback.answer()
    await callback.message.edit_text(ADD_NAME)

@add_recipe_router.message(ar.name)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ar.description)
    await message.answer(ADD_DESCRIPTION)

@add_recipe_router.message(ar.description)
async def get_inredients(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(ar.ingredients)
    await message.answer(ADD_INGREDIENTS)

@add_recipe_router.message(ar.ingredients)
async def get_steps_of_cooking(message: Message, state: FSMContext):
    await state.update_data(ingredients=message.text)
    await message.answer(ADD_STEPS)
    await state.set_state(ar.steps)

@add_recipe_router.message(ar.steps)
async def add_steps(message: Message, state: FSMContext):
    if len(message.text) > 5:
        await state.update_data(steps=message.text.strip())
        await make_card_of_dish_by_data_from_user(message, state)
    else:
        await message.answer(ERROR_SMALL_COUNT_OF_SYMBOLS_STEPS)


@add_recipe_router.callback_query(F.data == 'dont_add_recipe')
async def not_add_recipe(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(f"Рецепт не добавлен\n{MAIN_MENU}", reply_markup=main_menu)
    await state.clear()

@add_recipe_router.callback_query(F.data == 'add_recipe_to_database')
async def add_recipe(callback: CallbackQuery, state: FSMContext):
    await add_recipe_to_database(callback, state)
    await callback.answer()
    await callback.message.edit_text(f"Рецепт успешно добавлен!\n{MAIN_MENU}", reply_markup=main_menu)



