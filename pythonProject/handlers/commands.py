from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.messages import START_TEXT, SUPPORT, INSTRUCTION, MAIN_MENU, CHOOSE_CATEGORY, CATEGORY_OF_SAVED_RECIPES, GENERATE_OBJECT
from keybords import main_menu, back_to_main_menu, categories, categories_of_saved_recipes, generate_object
from states import TechnicalSupport as ts
from states import AddRecipe as ar
from database import set_user

start_router = Router()

@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer(START_TEXT, reply_markup=main_menu)
    await set_user(message.from_user.id)

@start_router.message(Command('support'))
async def technical_support_command(message: Message, state: FSMContext):
    await state.set_state(ts.mes)
    await message.answer(SUPPORT)

@start_router.message(Command('help'))
async def instruction_command(message: Message):
    await message.answer(INSTRUCTION, reply_markup=back_to_main_menu)

@start_router.message(Command('menu'))
async def menu_command(message: Message):
    await message.answer(MAIN_MENU, reply_markup=main_menu)

@start_router.message(Command('add_recipe'))
async def add_recipe_command(message: Message, state: FSMContext):
    await message.answer(CHOOSE_CATEGORY, reply_markup=categories)
    await state.set_state(ar.category)

@start_router.message(Command('my_recipes'))
async def my_recipes_command(message: Message):
    await message.answer(CATEGORY_OF_SAVED_RECIPES, reply_markup=categories_of_saved_recipes)

@start_router.message(Command('generate_recipe'))
async def generate_recipe_command(message: Message):
    await message.answer(GENERATE_OBJECT, reply_markup=generate_object)
