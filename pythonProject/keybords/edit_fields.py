from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

async def choose_edit_field(callback: CallbackQuery):
    recipe_name = callback.data.split('_')[1]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Название', callback_data=f"edit_name_{recipe_name}"),
         InlineKeyboardButton(text='Описание', callback_data=f"edit_description_{recipe_name}")],
        [InlineKeyboardButton(text='Ингредиенты', callback_data=f"edit_ingredients_{recipe_name}"),
         InlineKeyboardButton(text='Шаги', callback_data=f"edit_steps_{recipe_name}")],
        [InlineKeyboardButton(text='Отмена', callback_data=f"recipe_{recipe_name}")]
    ])

    return keyboard

finish_edit_steps = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Закончить', callback_data='finish_edit_steps')]
])