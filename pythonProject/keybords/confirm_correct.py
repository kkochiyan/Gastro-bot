from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def confirm_redact_recipe_keyboard(name: str):
    confirm = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'confirm_redact')],
        [InlineKeyboardButton(text='❌ Отмена', callback_data=f'recipe_{name}')]
    ])

    return confirm

def confirm_delete_recipe_keyboard(name: str, recipe_id: str):
    confirm = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'confirm_delete_{name}_{recipe_id}')],
        [InlineKeyboardButton(text='❌ Отмена', callback_data=f'recipe_{name}')]
    ])

    return confirm

