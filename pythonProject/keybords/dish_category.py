from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

categories = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Закуска 🍢', callback_data='category_snack'),
     InlineKeyboardButton(text='Салат 🥗', callback_data='category_salat')],
    [InlineKeyboardButton(text='Суп 🍲', callback_data='category_soup'),
     InlineKeyboardButton(text='Основное блюдо 🍛', callback_data='category_main')],
    [InlineKeyboardButton(text='Гарнир 🍚', callback_data='category_garnish'),
     InlineKeyboardButton(text='Соус или заправка 🧂', callback_data='category_sauce')],
    [InlineKeyboardButton(text='Выпечка 🍞', callback_data='category_bakery'),
     InlineKeyboardButton(text='Десерт 🍰', callback_data='category_desert')],
    [InlineKeyboardButton(text='Напиток 🍹', callback_data='category_drink'),
     InlineKeyboardButton(text='Консервация 🥫', callback_data='category_conservation')],
])

categories_of_saved_recipes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Закуски 🍢', callback_data='dish_snack'),
     InlineKeyboardButton(text='Салаты 🥗', callback_data='dish_salat')],
    [InlineKeyboardButton(text='Супы 🍲', callback_data='dish_soup'),
     InlineKeyboardButton(text='Основное блюда 🍛', callback_data='dish_main')],
    [InlineKeyboardButton(text='Гарниры 🍚', callback_data='dish_garnish'),
     InlineKeyboardButton(text='Соусы и заправки 🧂', callback_data='dish_sauce')],
    [InlineKeyboardButton(text='Выпечка 🍞', callback_data='dish_bakery'),
     InlineKeyboardButton(text='Десерты 🍰', callback_data='dish_desert')],
    [InlineKeyboardButton(text='Напитоки 🍹', callback_data='dish_drink'),
     InlineKeyboardButton(text='Консервации 🥫', callback_data='dish_conservation')],
    [InlineKeyboardButton(text='⏪️ Назад', callback_data='back_to_main_menu')]
])