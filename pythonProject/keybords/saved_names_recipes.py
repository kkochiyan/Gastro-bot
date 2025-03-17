from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

from database import get_names_recipes
from bot.messages import SAVED_RECIPES_IN_NEED_CATEGORY, CATEGORY_OF_SAVED_RECIPES
from keybords import categories_of_saved_recipes

async def saved_names_recipes_in_need_category(callback: CallbackQuery, category):
    saved_names = await get_names_recipes(callback, category)
    if saved_names:
        keyboard = InlineKeyboardBuilder()

        for name in saved_names:
            keyboard.add(InlineKeyboardButton(text=f"🧾 {name[0]}", callback_data=f"recipe_{name[0]}_{name[1]}"))

        keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_categories'))

        await callback.message.edit_text(SAVED_RECIPES_IN_NEED_CATEGORY,
                                            reply_markup=keyboard.adjust(2).as_markup())
    else:
        await callback.message.edit_text(
            f"В категории {category} у вас нет сохраненных рецептов.\n{CATEGORY_OF_SAVED_RECIPES}",
            reply_markup=categories_of_saved_recipes)


