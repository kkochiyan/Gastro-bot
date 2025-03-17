from bot.messages import MAIN_MENU
from database.models import async_session
from database.models import User, Category, Recipe
from keybords import main_menu
from states import EditRecipeState as er

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, func, and_, delete, update
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def add_recipe_to_database(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    tg_id = callback.from_user.id
    category_name = data.get('category')
    recipe_name = data.get('name')
    description = data.get('description')
    ingredients = data.get('ingredients')
    steps = data.get('steps')

    async with async_session() as session:
        query = select(Category).where(Category.name == category_name)
        result = await session.execute(query)
        category = result.scalar_one_or_none()

        if not category:
            category = Category(name=category_name)
            session.add(category)
            await session.flush()

        new_recipe = Recipe(
            user_id=tg_id,
            name=recipe_name,
            description=description,
            ingredients=ingredients,
            category_id=category.id,
            steps=steps
        )

        session.add(new_recipe)
        await session.commit()

        await state.clear()


async def get_names_recipes(callback: CallbackQuery, category: str):
    tg_id = callback.from_user.id

    async with async_session() as session:
        result = await session.execute(
            select(Recipe.name, Recipe.id).join(Category, Recipe.category_id == Category.id).
            where(and_(Recipe.user_id == tg_id, func.lower(Category.name) == category.lower()))
        )

        return result.all()

async def get_data_for_card_of_dish(callback: CallbackQuery):
    tg_id = callback.from_user.id
    recipe_name = callback.data.split('_')[1]

    async with async_session() as session:
        query = (
            select(
                Recipe.id,
                Recipe.name,
                Recipe.description,
                Recipe.ingredients,
                Recipe.steps,
                Category.name.label('category_name'),
            )
            .join(Category, Recipe.category_id == Category.id)
            .where(and_(Recipe.user_id == tg_id, Recipe.name == recipe_name))
        )

        result = await session.execute(query)
        rows = result.all()

    if not rows:
        return None

    return rows

async def delete_need_recipe(callback: CallbackQuery):
    tg_id = callback.from_user.id
    _, _, recipe_name, recipe_id = callback.data.split('_')
    print(recipe_id)

    async with async_session() as session:
        query = (
            delete(Recipe).where(and_(Recipe.user_id == tg_id, Recipe.name == recipe_name, Recipe.id == int(recipe_id)))
        )
        result = await session.execute(query)

        await session.commit()


async def get_data_for_cook(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    recipe_name = callback.data.split('_')[1]

    async with async_session() as session:
        result = await session.execute(
            select(Recipe.id, Recipe.description, Recipe.ingredients, Recipe.steps)
            .where(and_(Recipe.user_id == tg_id, Recipe.name == recipe_name))
        )
        recipe = result.first()

        recipe_id, description, ingredients, steps = recipe

    await state.update_data(recipe_name=recipe_name, description=description, ingredients=ingredients, steps=steps, step_index=-1)

#ToDo сделать функцию редактирования более удобной, поменять структуру бд, объеденить запросы по генерации рецептов по описанию и названию в одно, попробовать реализовать генерацию по фото
async def get_values_from_edit_field(callback: CallbackQuery, state: FSMContext):
    from keybords import get_keyboard_for_edit_steps, get_keyboard_for_edit_ingredients

    _, field, recipe_name = callback.data.split('_')
    tg_id = callback.from_user.id
    await state.update_data(field=field, recipe_name=recipe_name)

    async with async_session() as session:
        if field == 'name':
            await callback.message.edit_text(f'Вот текущее имя блюда: {recipe_name}.\n\nВведите новое название блюда.')
            await state.set_state(er.recipe_name)
            await state.update_data(name=recipe_name)
        elif field == 'description':
            desc =await session.scalar(
                select(Recipe.description).where(and_(Recipe.user_id == tg_id, func.lower(Recipe.name) == recipe_name.lower()))
            )
            await callback.message.edit_text(f'Вот текущее описание блюда: {desc}\n\nВведите новое описание блюда.')
            await state.set_state(er.recipe_description)
            await state.update_data(description=desc)
        elif field == 'ingredients':
            ing =await session.scalar(
                select(Recipe.ingredients).where(and_(Recipe.user_id == tg_id, func.lower(Recipe.name) == recipe_name.lower()))
            )
            await callback.message.edit_text(f'Вот текущие ингредиенты блюда:\n{ing}\n\nВыберите, какой ингредиент хотите редактировать.', reply_markup=get_keyboard_for_edit_ingredients(ing.split('\n'), recipe_name=recipe_name))
            await state.update_data(ingredients=ing.split('\n'))
        else:
            steps =await session.scalar(
                select(Recipe.steps)
                .where(and_(func.lower(Recipe.name) == recipe_name.lower(), Recipe.user_id == tg_id))
            )

            steps_lst = steps.split('\n')
            for i in range(len(steps_lst)):
                steps_lst[i] = f'{i+1}. {steps_lst[i]}'

            await callback.message.edit_text(text=f'Вот текущие щаги приготовления:\n{steps_lst}\n\nВыберите, какой шаг хотите редактировать.', reply_markup=get_keyboard_for_edit_steps(steps.split('\n'), recipe_name=recipe_name))
            await state.update_data(steps=steps.split('\n'))

async def update_data(callabck: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    field = data['field']
    tg_id = callabck.from_user.id
    recipe_name = data['recipe_name']

    async with async_session() as session:
        recipe = await session.scalar(
            select(Recipe).where(and_(func.lower(Recipe.name) == recipe_name.lower(), Recipe.user_id == tg_id))
        )

        if field == 'name':
            new_recipe_name = data['new_recipe_name']
            query = (
                update(Recipe)
                .where(and_(func.lower(Recipe.name) == recipe_name.lower(), Recipe.user_id == tg_id))
                .values(name=new_recipe_name)
            )

            res = await session.execute(query)
            await session.commit()

        elif field == 'description':
            new_description = data['new_description']
            query = (
                update(Recipe)
                .where(and_(func.lower(Recipe.name) == recipe_name.lower(), Recipe.user_id == tg_id))
                .values(description=new_description)
            )

            res = await session.execute(query)
            await session.commit()

        elif field == 'ingredients':
            new_ingredient = data['new_ingredient']
            cur_ingredient = data['cur_ingredient']

            current_ingredients = recipe.ingredients
            new_ingredients = current_ingredients.replace(cur_ingredient, new_ingredient)

            query = (
                update(Recipe)
                .where(and_(func.lower(Recipe.name) == recipe_name.lower(), Recipe.user_id == tg_id))
                .values(ingredients=new_ingredients)
            )

            res = await session.execute(query)
            await session.commit()

        else:
            new_step = data['new_step']
            cur_step = data['cur_step']

            current_steps = recipe.steps
            new_steps = current_steps.replace(cur_step, new_step)

            query = (
                update(Recipe)
                .where(and_(func.lower(Recipe.name) == recipe_name.lower(), Recipe.user_id == tg_id))
                .values(steps=new_steps)
            )

            res = await session.execute(query)
            await session.commit()

async def get_recipe(tg_id: int, recipe_name: str):
    async with async_session() as session:
        res = await session.execute(
            select(Recipe).where(and_(Recipe.user_id == tg_id, func.lower(Recipe.name) == recipe_name.lower()))
        )
        return res.scalar_one_or_none()

async def update_new_ingredients(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        data = await state.get_data()
        recipe_name = data["recipe_name"]
        position = data["position"]
        new_ingredient = data["new_ingredient"]

        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if recipe:
            ingredients = recipe.ingredients.split("\n")
            ingredients.insert(position, new_ingredient)
            recipe.ingredients = "\n".join(ingredients)
            await session.commit()

            await callback.message.edit_text(f"✅ *{new_ingredient}* добавлен на позицию {position + 1}.\n\n{MAIN_MENU}",
                                             parse_mode="Markdown",
                                             reply_markup=main_menu)
        else:
            await callback.message.answer("Ошибка: рецепт не найден.")

        await state.clear()

async def update_new_steps(callback: CallbackQuery, state: FSMContext):
    async with async_session() as session:
        data = await state.get_data()
        recipe_name = data["recipe_name"]
        position = data["position"]
        new_step = data["new_steps"]

        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if recipe:
            steps = recipe.steps.split("\n")
            steps.insert(position, new_step)
            recipe.ingredients = "\n".join(steps)
            await session.commit()

            await callback.message.edit_text(f"✅ *{new_step}* добавлен на позицию {position + 1}.\n\n{MAIN_MENU}",
                                             parse_mode="Markdown",
                                             reply_markup=main_menu)
        else:
            await callback.message.answer("Ошибка: рецепт не найден.")

        await state.clear()

async def get_ingredients_for_delete(callback: CallbackQuery):
    await callback.answer()
    _, _, recipe_name = callback.data.split('_')

    async with async_session() as session:

        # Получаем рецепт из базы данных
        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if not recipe:
            await callback.message.answer("Ошибка: рецепт не найден.")
            return

        ingredients = recipe.ingredients.split("\n")

        if not ingredients:
            await callback.message.answer("В этом рецепте нет ингредиентов.")
            return

        # Создаем кнопки с ингредиентами для выбора удаления
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"❌ {ingredient}", callback_data=f"confirm_del_ingredient_{recipe_name}_{i}")]
            for i, ingredient in enumerate(ingredients)
        ])
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="🔙 Отмена", callback_data=f"edit_ingredients_{recipe_name}")])

        await callback.message.edit_text(f"Вот текущие ингредиенты:\n{'\n'.join(ingredients)}\n\nВыберите ингредиент для удаления:", reply_markup=keyboard)

async def confirm_delete_need_ingredient(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    _, _, _, recipe_name, index = callback.data.split('_')
    index = int(index)

    async with async_session() as session:
            # Получаем рецепт
            result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
            recipe = result.scalar_one_or_none()

            if not recipe:
                await callback.message.answer("Ошибка: рецепт не найден.")
                return

            ingredients = recipe.ingredients.split("\n")

            if index >= len(ingredients):
                await callback.message.answer("Ошибка: индекс ингредиента неверный.")
                return

            ingredient_to_delete = ingredients[index]

            new_ingredients = ingredients[:index] + ingredients[index + 1:]

            old_text = "\n".join(f"{i + 1}. {ing}" for i, ing in enumerate(ingredients))
            new_text = "\n".join(f"{i + 1}. {ing}" for i, ing in enumerate(new_ingredients))

            await state.update_data(recipe_name=recipe_name, ingredient_to_delete=ingredient_to_delete, index=index)

            await callback.message.edit_text(
                f"*🔄 Удаление ингредиента:*\n\n"
                f"*📌 БЫЛО:*\n{old_text}\n\n"
                f"*✅ СТАЛО:*\n{new_text}\n\n"
                f"Удалить ингредиент: {ingredient_to_delete}?",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="✅ Да", callback_data="execute_delete_ingredient")],
                    [InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel_delete_ingredient")]
                ])
            )

async def delete_need_ingredient(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Ингредиент удалён')
    data = await state.get_data()
    recipe_name = data["recipe_name"]
    index = data["index"]

    async with async_session() as session:
        # Получаем рецепт
        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if not recipe:
            await callback.message.answer("Ошибка: рецепт не найден.")
            await state.clear()
            return

        ingredients = recipe.ingredients.split("\n")

        if index >= len(ingredients):
            await callback.message.answer("Ошибка: ингредиент уже удалён или индекс неверный.")
            await state.clear()
            return

        del ingredients[index]
        recipe.ingredients = "\n".join(ingredients)

        await session.commit()
        await state.clear()

        await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu)

async def choose_ingredient_to_redact(callback: CallbackQuery):
    await callback.answer()
    _, _, recipe_name = callback.data.split('_')

    async with async_session() as session:
        # Получаем рецепт из базы данных
        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if not recipe:
            await callback.message.answer("Ошибка: рецепт не найден.")
            return

        ingredients = recipe.ingredients.split("\n")

        if not ingredients:
            await callback.message.answer("В этом рецепте нет ингредиентов.")
            return

        # Создаем кнопки с ингредиентами для выбора редактирования
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"✏ {ingredient}", callback_data=f"edit_ingredient_{recipe_name}_{i}")]
            for i, ingredient in enumerate(ingredients)
        ])
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text="🔙 Отмена", callback_data=f"edit_ingredients_{recipe_name}")])

        await callback.message.edit_text("Выберите ингредиент для редактирования:", reply_markup=keyboard)

async def confirm_ingredient_redact(message: Message, state: FSMContext):
    async with async_session() as session:
        new_ingredient = message.text
        data = await state.get_data()
        recipe_name = data["recipe_name"]
        index = data["index"]

        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if not recipe:
            await message.answer("Ошибка: рецепт не найден.")
            await state.clear()
            return

        ingredients = recipe.ingredients.split("\n")

        if index >= len(ingredients):
            await message.answer("Ошибка: индекс ингредиента неверный.")
            await state.clear()
            return

        old_ingredient = ingredients[index]
        new_ingredients = ingredients[:]
        new_ingredients[index] = new_ingredient

        old_text = "\n".join(f"{i + 1}. {ing}" for i, ing in enumerate(ingredients))
        new_text = "\n".join(f"{i + 1}. {ing}" for i, ing in enumerate(new_ingredients))

        await state.update_data(new_ingredient=new_ingredient)

        await message.answer(
            f"*🔄 Изменение ингредиента:*\n\n"
            f"*📌 БЫЛО:*\n{old_text}\n\n"
            f"*✅ СТАЛО:*\n{new_text}\n\n"
            f"Заменить {old_ingredient} на {new_ingredient}?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Да", callback_data="confirm_ingredient_update")],
                [InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancle_update")]
            ])
        )

async def update_ingredients(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Ингредиент обновлён')
    data = await state.get_data()
    recipe_name = data["recipe_name"]
    index = data["index"]
    new_ingredient = data["new_ingredient"]

    async with async_session() as session:
        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if not recipe:
            await callback.message.answer("Ошибка: рецепт не найден.")
            await state.clear()
            return

        ingredients = recipe.ingredients.split("\n")

        if index >= len(ingredients):
            await callback.message.answer("Ошибка: ингредиент уже изменён или индекс неверный.")
            await state.clear()
            return

        ingredients[index] = new_ingredient
        recipe.ingredients = "\n".join(ingredients)

        await session.commit()
        await state.clear()

        await callback.message.edit_text(MAIN_MENU, reply_markup=main_menu)

async def confirm_addition_ing(message: Message, state: FSMContext):
    new_ingredient = message.text
    data = await state.get_data()
    recipe_name = data["recipe_name"]
    position = data["position"]

    async with async_session() as session:
        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if recipe:
            old_ingredients = recipe.ingredients.split("\n")
            new_ingredients = old_ingredients[:]
            new_ingredients.insert(position, new_ingredient)

            old_text = "\n".join(f"{i + 1}. {ing}" for i, ing in enumerate(old_ingredients))
            new_text = "\n".join(f"{i + 1}. {ing}" for i, ing in enumerate(new_ingredients))

            # Отправляем подтверждение перед сохранением
            await state.update_data(new_ingredient=new_ingredient)
            await message.answer(
                f"*🔄 Изменение списка ингредиентов:*\n\n"
                f"*📌 БЫЛО:*\n{old_text}\n\n"
                f"*✅ СТАЛО:*\n{new_text}\n\n"
                "Сохранить изменения?",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="✅ Да", callback_data="confirm_add_ingredient")],
                    [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_add_ingredient")]
                ])
            )
        else:
            await message.answer("Ошибка: рецепт не найден.")
            await state.clear()


async def confirm_addition_step(message: Message, state: FSMContext):
    new_step = message.text
    data = await state.get_data()
    recipe_name = data["recipe_name"]
    position = data["position"]

    async with async_session() as session:
        result = await session.execute(select(Recipe).where(Recipe.name == recipe_name))
        recipe = result.scalar_one_or_none()

        if recipe:
            old_steps = recipe.steps.split("\n")
            new_steps = old_steps[:]
            new_steps.insert(position, new_step)

            old_text = "\n".join(f"{i + 1}. {ing}" for i, ing in enumerate(old_steps))
            new_text = "\n".join(f"{i + 1}. {ing}" for i, ing in enumerate(new_steps))

            # Отправляем подтверждение перед сохранением
            await state.update_data(new_steps=new_step)
            await message.answer(
                f"*🔄 Изменение списка шагов приготовлений:*\n\n"
                f"*📌 БЫЛО:*\n{old_text}\n\n"
                f"*✅ СТАЛО:*\n{new_text}\n\n"
                "Сохранить изменения?",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="✅ Да", callback_data="confirm_add_step")],
                    [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_add_step")]
                ])
            )
        else:
            await message.answer("Ошибка: рецепт не найден.")
            await state.clear()