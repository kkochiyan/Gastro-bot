from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

generate_object = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='По фото', callback_data='generate_photo')],
    [InlineKeyboardButton(text='По названию', callback_data='generate_name')],
    [InlineKeyboardButton(text='По описанию', callback_data='generate_description')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main_menu')]
])