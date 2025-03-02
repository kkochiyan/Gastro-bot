from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

add_recipe_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Добавить рецепт', callback_data='add_recipe_to_database')],
    [InlineKeyboardButton(text='❌ Не добавлять рецепт', callback_data='dont_add_recipe')]
])