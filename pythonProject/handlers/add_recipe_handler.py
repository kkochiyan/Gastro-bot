from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states import AddRecipe as ar
from bot.messages import CHOOSE_CATEGORY, MAIN_MENU
from keybords import categories, main_menu
from utils import category_defenition, make_card_of_dish_by_data_from_user, data_validation_check
from database import add_recipe_to_database

add_recipe_router = Router()

LIMIT_NAME = 100
LIMIT_DESC = 500
LIMIT_INGR = 2000
LIMIT_STEPS = 5000

@add_recipe_router.callback_query(F.data == 'add_recipe')
async def get_dish_category(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('Выбери категорию блюда.', reply_markup=categories)
    await state.set_state(ar.category)

@add_recipe_router.callback_query(F.data.startswith('category_'))
async def get_dish_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=category_defenition(callback.data.split('_')[1]))
    await state.set_state(ar.name)
    await callback.answer()
    await callback.message.edit_text('Введите название блюда (до 100 символов).')

@add_recipe_router.message(ar.name)
async def get_description(message: Message, state: FSMContext):
    name = message.text.strip()
    if data_validation_check(name, LIMIT_NAME):
        await message.answer('Название слишком длинное! Введите, пожалуйста не более 100 символов.')
        return
    await state.update_data(name=name)
    await state.set_state(ar.description)
    await message.answer('Отлично! Теперь введите описание блюда (до 500 символов).')

@add_recipe_router.message(ar.description)
async def get_inredients(message: Message, state: FSMContext):
    desc = message.text.strip()
    if data_validation_check(desc, LIMIT_DESC):
        await message.answer('Описание слишком длинное! Введите, пожалуйста, не более 500 символов.')
        return
    await state.update_data(description=desc)
    await state.set_state(ar.ingredients)
    await message.answer('Теперь необходимо ввести ингредиенты (до 2000 символов) построчно, например:\n'
                         'Яйца 3 шт.\nМолоко 1 л.\nМука 200 гр.')


@add_recipe_router.message(ar.ingredients)
async def get_steps_of_cooking(message: Message, state: FSMContext):
    ing = message.text.strip()
    if data_validation_check(ing, LIMIT_INGR):
        await message.answer('Слишком много текста! Введите, пожалуйста, не более 2000 символов.')
        return
    await state.update_data(ingredients=ing)
    await message.answer('Почти все. Осталось только ввести шаги приготовления.'
                         'Введите шаги приготовления (до 5000 символов) построчно, например:\n'
                         'Шаг 1\nШаг 2\nШаг 3')
    await state.set_state(ar.steps)

@add_recipe_router.message(ar.steps)
async def add_steps(message: Message, state: FSMContext):
    steps = message.text.strip()
    if data_validation_check(steps, LIMIT_STEPS):
        await message.answer('Шаги приготовления слишком длинные! Введите, пожалуйста, не более 5000 символов.')
        return
    await state.update_data(steps=message.text.strip())
    await make_card_of_dish_by_data_from_user(message, state)


@add_recipe_router.callback_query(F.data == 'dont_add_recipe')
async def not_add_recipe(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Рецепт не сохранен')
    await callback.message.edit_text(f"{MAIN_MENU}", reply_markup=main_menu)
    await state.clear()

@add_recipe_router.callback_query(F.data == 'add_recipe_to_database')
async def add_recipe(callback: CallbackQuery, state: FSMContext):
    await add_recipe_to_database(callback, state)
    await callback.answer('Рецепт успешно сохранен')
    await callback.message.edit_text(f"{MAIN_MENU}", reply_markup=main_menu)



