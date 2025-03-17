from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='➕🍽️ Добавить рецепт', callback_data='add_recipe')],
    [InlineKeyboardButton(text='📂🍲 Сохраненные рецепты', callback_data='saved_recipes')],
    [InlineKeyboardButton(text='🤖🍽️ Сгенерировать рецепт', callback_data='generate_recipe')],
    [InlineKeyboardButton(text='🆘💬 Тех поддержка', callback_data='technical_support')]
])