from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Салат', callback_data='category_salat')],
    [InlineKeyboardButton(text='Первое блюдо', callback_data='category_first')],
    [InlineKeyboardButton(text='Второе блюдо', callback_data='category_second')],
    [InlineKeyboardButton(text='Десерт', callback_data='category_dessert')],
    [InlineKeyboardButton(text='Напиток', callback_data='category_drink')]
])

categories_of_saved_recipes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Салаты', callback_data='dish_salat')],
    [InlineKeyboardButton(text='Первые блюда', callback_data='dish_first')],
    [InlineKeyboardButton(text='Вторые блюда', callback_data='dish_second')],
    [InlineKeyboardButton(text='Десерты', callback_data='dish_dessert')],
    [InlineKeyboardButton(text='Напитки', callback_data='dish_drink')],
    [InlineKeyboardButton(text='Назад', callback_data='back_to_main_menu')]
])