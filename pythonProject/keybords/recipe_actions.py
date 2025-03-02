from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


async def recipe_actions(category_name, recipe_name):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Начать готовку', callback_data=f"start_{recipe_name}")],
        [InlineKeyboardButton(text='Редактировать', callback_data=f"correct_{recipe_name}")],
        [InlineKeyboardButton(text='Удалить', callback_data=f"delete_{recipe_name}")],
        [InlineKeyboardButton(text='Назад', callback_data=f"dish_{category_name}")]
    ])

    return keyboard