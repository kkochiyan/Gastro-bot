from database.models import async_session
from database.models import User, Category, Recipe, Step

from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, func, and_, delete, update

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
            category_id=category.id
        )
        session.add(new_recipe)
        await session.flush()

        step_objects = [
            Step(recipe_id=new_recipe.id, step_number=i + 1, description=step_text)
            for i, step_text in enumerate(steps)
        ]
        session.add_all(step_objects)

        await session.commit()

        await state.clear()


async def get_names_recipes(callback: CallbackQuery, category: str):
    tg_id = callback.from_user.id

    async with async_session() as session:
        result = await session.scalars(
            select(Recipe.name).join(Category, Recipe.category_id == Category.id).
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
                Category.name.label('category_name'),
                Step.step_number,
                Step.description.label('step_description')
            )
            .join(Category, Recipe.category_id == Category.id)
            .outerjoin(Step, Recipe.id == Step.recipe_id)
            .where(and_(Recipe.user_id == tg_id, Recipe.name == recipe_name))
            .order_by(Step.step_number)
        )

        result = await session.execute(query)
        rows = result.all()

    if not rows:
        return None

    return rows

async def delete_need_recipe(callback: CallbackQuery):
    tg_id = callback.from_user.id
    recipe_name = callback.data.split('_')[1]

    async with async_session() as session:
        query = (
            delete(Recipe).where(and_(Recipe.user_id == tg_id, Recipe.name == recipe_name))
        )
        result = await session.execute(query)

        await session.commit()

        await callback.message.answer(f"Рецепт {recipe_name} успешно удален!")

async def update_data_values(message: Message, state: FSMContext):
    data = await state.get_data()
    tg_id = message.from_user.id
    recipe_name = data['recipe_name']
    field = data['field']

    new_value = message.text.strip()

    async with async_session() as session:
        query = update(Recipe).where(and_(Recipe.name == recipe_name, Recipe.user_id == tg_id)).values({field: new_value})
        await session.execute(query)
        await session.commit()

    await message.answer(f"{field.capitalize()} успешно обновлен!")
    await state.clear()

async def update_data_steps(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    tg_id = callback.from_user.id
    recipe_name = data['recipe_name']
    steps = data['steps']

    async with async_session() as session:
        result = await session.execute(
            select(Recipe.id).where(and_(Recipe.name == recipe_name, Recipe.user_id == tg_id))
        )
        recipe_id = result.scalar_one_or_none()

        await session.execute(delete(Step).where(Step.recipe_id == recipe_id))
        await session.commit()

        step_objects = [
            Step(recipe_id=recipe_id, step_number=i + 1, description=step_text)
            for i, step_text in enumerate(steps)
        ]
        session.add_all(step_objects)
        await session.commit()

    await callback.message.answer("Шаги обновлены!")
    await state.clear()

async def get_data_for_cook(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    recipe_name = callback.data.split('_')[1]

    async with async_session() as session:
        result = await session.execute(
            select(Recipe.id, Recipe.description, Recipe.ingredients).where(and_(Recipe.user_id == tg_id, Recipe.name == recipe_name))
        )
        recipe = result.first()

        recipe_id, description, ingredients = recipe

        steps_result = await session.execute(
            select(Step.step_number, Step.description).where(Step.recipe_id == recipe_id).order_by(Step.step_number)
        )

        steps = steps_result.fetchall()

    await state.update_data(recipe_name=recipe_name, description=description, ingredients=ingredients, steps=steps, step_index=-1)