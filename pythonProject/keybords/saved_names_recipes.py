from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

from database import get_names_recipes

async def saved_names_recipes(callback: CallbackQuery, category):
    saved_names = await get_names_recipes(callback, category)
    keyboard = InlineKeyboardBuilder()

    for name in saved_names:
        keyboard.add(InlineKeyboardButton(text=name, callback_data=f"recipe_{name}"))

    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_categories'))
    return keyboard.adjust(2).as_markup()
