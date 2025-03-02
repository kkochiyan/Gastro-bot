from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main_menu')]
])