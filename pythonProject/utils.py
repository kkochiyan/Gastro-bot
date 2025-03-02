from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.messages import NOT_STEPS, COMPLETE_ADD_STEP, EDIT_STEPS
from keybords import add_recipe_keyboard, finish_edit_steps, swith_between_steps
from states import EditRecipeState


async def process_recipe_step(message: Message, state: FSMContext, user_input: str):
    data = await state.get_data()
    steps = data.get("steps", [])

    if user_input.lower() == 'готово':
        if not steps:
            await message.answer(NOT_STEPS)
            return

        steps_list = '\n'.join([f"{i + 1}. {step}" for i, step in enumerate(steps)])
        category_of_dish = data['category']
        recipe_name = data['name']
        description = data['description']
        ingredients = data['ingredients']

        card_of_dish = (f"Категория блюда: {category_of_dish}\n\n"
                        f"Название блюда: {recipe_name}\n\n"
                        f"Описание: {description}\n\n"
                        f"Ингредиенты:\n{ingredients}\n\n"
                        f"Шаги приготовления:\n{steps_list}")

        await message.answer('Отлично, все данные получены')
        await message.answer(f"Вот ваша карточка блюда:\n\n{card_of_dish}", reply_markup=add_recipe_keyboard)

        return

    steps.append(user_input)
    await state.update_data(steps=steps)
    await message.answer(COMPLETE_ADD_STEP)


def category_defenition(cat):
    if cat == 'salat':
        return 'Салат'
    elif cat == 'first':
        return 'Первое блюдо'
    elif cat == 'second':
        return 'Второе блюдо'
    elif cat == 'dessert':
        return 'Десерт'
    else:
        return 'Напиток'

def make_card_of_dish(rows):
    recipe_card = {
        'category': rows[0].category_name,
        'name': rows[0].name,
        'description': rows[0].description,
        'ingredients': rows[0].ingredients,
        'steps': []
    }

    for row in rows:
        if row.step_number is not None:
            recipe_card['steps'].append({
                'number': row.step_number,
                'description': row.step_description
            })

    text = (
        f"Карточка блюда\n\n"
        f"Каьегория блюда: {recipe_card['category']}\n\n"
        f"Название блюда: {recipe_card['name']}\n\n"
        f"Описание блюда: {recipe_card['description']}\n\n"
        f"Ингредиенты: \n{recipe_card['ingredients']}\n\n"
        f"Шаги приготовления: \n"
    )

    for step in recipe_card['steps']:
        text += f"{step['number']}. {step['description']}\n"

    return text

async def choose_and_start_edit(callback: CallbackQuery, state: FSMContext):
    _, field, recipe_name = callback.data.split('_')

    await state.update_data(recipe_name=recipe_name, field=field)

    if field in ['name', 'description', 'ingredients']:
        field_names = {
            'name': 'Введите новое название рецепта:',
            'description': 'Введите новое описание рецепта:',
            'ingredients': 'введите новые ингредиенты построчной(каждый ингредиент с новой строки)'
        }
        await callback.message.edit_text(field_names[field])
        await state.set_state(EditRecipeState.waiting_for_new_value)

    else:
        await callback.message.edit_text(EDIT_STEPS)
        await state.update_data(steps=[])
        await state.set_state(EditRecipeState.waiting_for_steps)

async def recive_steps(message: Message, state: FSMContext):
    data = await state.get_data()
    data['steps'].append(message.text.strip())

    await message.answer('Добавлен! Отправьте следующий шаг или нажмите "Закончить"', reply_markup=finish_edit_steps)

async def send_cooking_steps(message: Message, state: FSMContext):
    data = await state.get_data()

    recipe_name = data['recipe_name']
    description = data['description']
    ingredients = data['ingredients']
    steps = data['steps']
    step_index = data['step_index']

    if step_index == -1:
        text = f"Отлично! Давай приготовим {recipe_name}.\n\n\nНазвание рецепта: {recipe_name}\n\nОписание рецепта: {description}\n\nИнгредиенты:\n{ingredients}"
    else:
        text = f"Шаг {steps[step_index][0]}\n\n{steps[step_index][1]}"

    await message.edit_text(text, reply_markup=await swith_between_steps(step_index, len(steps) - 1))
