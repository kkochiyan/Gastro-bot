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

def get_keyboard_for_edit_steps(steps, recipe_name):
    count_steps = len(steps)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Шаг {i+1}', callback_data=f'redact_step_{i+1}_{recipe_name}')]
            for i in range(count_steps)
        ]
    )

    return keyboard

def get_keyboard_for_edit_ingredients(ingredients, recipe_name):
    count_ingredients = len(ingredients)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f'Ингредиент {i+1}', callback_data=f'redact_ingredient_{i+1}_{recipe_name}')]
            for i in range(count_ingredients)
        ]
    )

    return keyboard

def choose_wich_type_of_correct_to_ingredients(recipe_name: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕ Добавить', callback_data=f"add_ingredient_{recipe_name}")],
        [InlineKeyboardButton(text='❌ Удалить', callback_data=f"del_ingredient_{recipe_name}")],
        [InlineKeyboardButton(text='✏ Редактировать', callback_data=f"update_ingredient_{recipe_name}")],
        [InlineKeyboardButton(text='🔙 Назад', callback_data=f"correct_{recipe_name}")]
    ])
    return keyboard

def choose_wich_type_of_correct_to_steps(recipe_name: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='➕ Добавить', callback_data=f"add_step_{recipe_name}")],
        [InlineKeyboardButton(text='❌ Удалить', callback_data=f"del_step_{recipe_name}")],
        [InlineKeyboardButton(text='✏ Редактировать', callback_data=f"redact_step_{recipe_name}")],
        [InlineKeyboardButton(text='🔙 Назад', callback_data=f"correct_{recipe_name}")]
    ])
    return keyboard

async def choose_position_to_add_ingredient(callback: CallbackQuery, ingredients):
    recipe_name = callback.data.split('_')[2]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 В начало",
                              callback_data=f"add_pos_ingredient_{recipe_name}_0")],
        [InlineKeyboardButton(text="📌 В конец",
                              callback_data=f"add_pos_ingredient_{recipe_name}_{len(ingredients)}")],
    ] + [
        [InlineKeyboardButton(text=f"После: {ingredient}",
                              callback_data=f"add_pos_ingredient_{recipe_name}_{i + 1}")]
        for i, ingredient in enumerate(ingredients)
    ] + [[InlineKeyboardButton(text="🔙 Назад",
                               callback_data=f"edit_ingredients_{recipe_name}")]])

    return keyboard

async def choose_position_to_add_step(callback: CallbackQuery, steps):
    recipe_name = callback.data.split('_')[2]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📌 В начало",
                              callback_data=f"add_pos_step_{recipe_name}_0")],
        [InlineKeyboardButton(text="📌 В конец",
                              callback_data=f"add_pos_step_{recipe_name}_{len(steps)}")],
    ] + [
        [InlineKeyboardButton(text=f"После: {steps}",
                              callback_data=f"add_pos_step_{recipe_name}_{i + 1}")]
        for i, ingredient in enumerate(steps)
    ] + [[InlineKeyboardButton(text="🔙 Назад",
                               callback_data=f"edit_steps_{recipe_name}")]])

    return keyboard