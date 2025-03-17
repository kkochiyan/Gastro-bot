from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.messages import START_TEXT, SUPPORT, INSTRUCTION, MAIN_MENU
from keybords import main_menu, back_to_main_menu
from states import TechnicalSupport as ts
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


