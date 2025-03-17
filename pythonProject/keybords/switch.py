from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def swith_between_steps(step_index, lenght):
    if step_index == -1:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Вперед ⏩️', callback_data='next_step')],
            [InlineKeyboardButton(text='🏁👨‍🍳 Закончить готовку', callback_data='finish_cook')]
        ])
        return keyboard
    elif step_index == lenght:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='⏪️ Назад', callback_data='prev_step')],
            [InlineKeyboardButton(text='🏁👨‍🍳 Закончить готовку', callback_data='finish_cook')]
        ])
        return keyboard
    elif step_index >= 0:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='⏪️ Назад', callback_data='prev_step'),
             InlineKeyboardButton(text='Вперед ⏩️', callback_data='next_step')],
            [InlineKeyboardButton(text='🏁👨‍🍳 Закончить готовку', callback_data='finish_cook')]
        ])
        return keyboard
