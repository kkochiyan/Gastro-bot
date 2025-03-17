from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

save_generated_recipe_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Сохранить рецепт', callback_data='save_recipe_to_database')],
    [InlineKeyboardButton(text='❌ Не сохранять рецпт', callback_data='dont_save_recipe')]
])
