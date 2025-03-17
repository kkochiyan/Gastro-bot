from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

generate_object = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='По фото', callback_data='generate_photo')],
    [InlineKeyboardButton(text='По названию или описанию', callback_data='generate_name_or_description')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main_menu')]
])