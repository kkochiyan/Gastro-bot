from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re

from keybords import add_recipe_keyboard

#Оптимизированная
async def make_card_of_dish_by_data_from_user(message: Message, state: FSMContext):
    data = await state.get_data()

    steps = "\n".join(f"{i+1}. {step.strip()}" for i, step in enumerate(data['steps'].split("\n")) if step.strip())

    recipe_card = f"""🍽 *Карточка блюда* 🍽

📌 *Категория:* {data['category']}
📛 *Название:* {data['name']}

📖 *Описание:*
{data['description']}

🥩 *Ингредиенты:*
{data['ingredients']}

👨‍🍳 *Шаги приготовления:*
{steps}"""

    await message.answer("Отлично! Все данные получены, загружаем карточку блюда...")
    await message.answer(recipe_card, reply_markup=add_recipe_keyboard, parse_mode="Markdown")

#Оптимизированная
def category_defenition(cat):
    if cat == 'salat':
        return 'Салат'
    elif cat == 'snack':
        return 'Закуска'
    elif cat == 'soup':
        return 'Суп'
    elif cat == 'main':
        return 'Основное блюдо'
    elif cat == 'garnish':
        return 'Гарнир'
    elif cat == 'sauce':
        return 'Соус или заправка'
    elif cat == 'backery':
        return 'Выпечка'
    elif cat == 'desert':
        return 'Основное блюдо'
    elif cat == 'conservation':
        return 'Консервация'
    else:
        return 'Напиток'

def make_card_of_dish_by_data_from_database(rows):
    recipe_card = {
        'category': rows[0].category_name,
        'name': rows[0].name,
        'description': rows[0].description,
        'ingredients': rows[0].ingredients,
    }

    steps = rows[0].steps.split('\n')

    for i in range(len(steps)):
        steps[i] = f'{i+1}. {steps[i]}'

    text = (
        f"Карточка блюда\n\n"
        f"Каьегория блюда: {recipe_card['category']}\n\n"
        f"Название блюда: {recipe_card['name']}\n\n"
        f"Описание блюда: {recipe_card['description']}\n\n"
        f"Ингредиенты: \n{recipe_card['ingredients']}\n\n"
        f"Шаги приготовления:\n{'\n'.join(steps)}"
    )

    return text

async def send_cooking_steps(message: Message, state: FSMContext):
    from keybords import swith_between_steps

    data = await state.get_data()

    recipe_name = data['recipe_name']
    description = data['description']
    ingredients = data['ingredients']
    steps = data['steps'].split('\n')
    step_index = data['step_index']


    if step_index == -1:
        text = f"Отлично! Давай приготовим {recipe_name}.\n\n\nНазвание рецепта: {recipe_name}\n\nОписание рецепта: {description}\n\nИнгредиенты:\n{ingredients}"
    else:
        text = f"Шаг {step_index + 1}\n\n{steps[step_index]}"

    await message.edit_text(text, reply_markup=await swith_between_steps(step_index, len(steps) - 1))

#Оптимизированная
async def parse_recipe(state: FSMContext, response_text):
    response_text = response_text.strip()

    category_match = re.search(r'Категория:\s*(.+)', response_text)
    name_match = re.search(r'Название:\s*(.+)', response_text)
    description_match = re.search(r'Описание:\s*(.+)', response_text)

    category = category_match.group(1).strip() if category_match else None
    name = name_match.group(1).strip() if name_match else None
    description = description_match.group(1).strip() if description_match else None

    ingredients_match = re.search(r'Ингредиенты:\s*\n(.+?)\n\nШаги приготовления:', response_text, re.S)
    ingredients = []
    if ingredients_match:
        raw_ingredients = ingredients_match.group(1).strip().split("\n")
        ingredients = [re.sub(r'^[\-\*\d.\s]+', '', ing).strip() for ing in raw_ingredients]  # Убираем маркеры списка

    steps_match = re.search(r'Шаги приготовления:\s*\n(.+)', response_text, re.S)
    steps = []
    if steps_match:
        raw_steps = steps_match.group(1).strip().split("\n")
        for step in raw_steps:
            cleaned_step = re.sub(r'^\d+\.\s*', '', step).strip()  # Убираем номера
            steps.append(cleaned_step)

    await state.update_data(category=category, name=name, description=description, ingredients='\n'.join(ingredients), steps='\n'.join(steps))

async def confirm_correct_value(message: Message, state: FSMContext):
    from keybords import confirm_redact_recipe_keyboard

    data = await state.get_data()
    field = data['field']

    if field == 'name':
        cur_value = data['name']
        new_value = data['new_recipe_name']

    elif field == 'description':
        cur_value = data['description']
        new_value = data['new_description']

    elif field == 'ingredients':
        cur_value = data['cur_ingredient']
        new_value = data['new_ingredient']

    else:
        cur_value = data['cur_step']
        new_value = data['new_step']


    await message.answer(f'Вот текущее значение: {cur_value}\n\nВот отредактированное значение: {new_value}\n\nПодтвердить изменения?',
                         reply_markup=confirm_redact_recipe_keyboard(data['recipe_name']))

#Оптимизированная
def data_validation_check(data: str, limit: int):
    return len(data) > limit






