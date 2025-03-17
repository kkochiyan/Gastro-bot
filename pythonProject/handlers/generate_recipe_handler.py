from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.messages import GENERATE_OBJECT, GENERATE_BY_NAME, get_promt, MAIN_MENU
from keybords import generate_object, save_generated_recipe_keyboard, main_menu
from states import GenerateObject
from requests_to_GigaChat import generate_recipe_with_GigaChat, generate_recipe_with_deepseek, \
    generate_recipe_with_yabdex
from utils import parse_recipe
from database import add_recipe_to_database

generate_recipe_router = Router()

@generate_recipe_router.callback_query(F.data == 'generate_recipe')
async def choose_generate_object(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(GENERATE_OBJECT, reply_markup=generate_object)

@generate_recipe_router.callback_query(F.data == 'generate_name_or_description')
async def get_name_for_generate(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(GENERATE_BY_NAME)
    await state.set_state(GenerateObject.name_or_description)

@generate_recipe_router.message(GenerateObject.name_or_description)
async def get_generated_recipe_by_name(message: Message, state: FSMContext):
    recipe = await generate_recipe_with_GigaChat(get_promt(title_or_description=message.text.strip()))
    await parse_recipe(state, recipe)
    await message.answer(recipe, reply_markup=save_generated_recipe_keyboard)

@generate_recipe_router.callback_query(F.data == 'dont_save_recipe')
async def dont_save_generated_recipe(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Рецепт не сохранен')
    await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu)
    await state.clear()

@generate_recipe_router.callback_query(F.data == 'save_recipe_to_database')
async def save_generated_recipe_to_main_database(callback: CallbackQuery, state: FSMContext):
    await add_recipe_to_database(callback=callback, state=state)
    await callback.answer('Рецепт успешно добавлен!')
    await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu)




