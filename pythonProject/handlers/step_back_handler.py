from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.messages import MAIN_MENU, CATEGORY_OF_SAVED_RECIPES
from keybords import main_menu, categories_of_saved_recipes

step_back_router = Router()

@step_back_router.callback_query(F.data == 'back_to_main_menu')
async def back_to_main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu)

@step_back_router.callback_query(F.data == 'back_to_categories')
async def back_to_categories(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(CATEGORY_OF_SAVED_RECIPES, reply_markup=categories_of_saved_recipes)