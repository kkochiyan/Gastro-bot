from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.messages import SORRY, MAIN_MENU
from keybords import main_menu

waste_messages_router = Router()

# @waste_messages_router.message(F.text)
# async def connect_with_menu(message: Message, state: FSMContext):
#     #await state.clear()
#     cur_state = await state.get_state()
#     print(f'Неожиданное сообщение, текущее состояние: {cur_state}')
#     await message.answer(f"{SORRY}\n\n{MAIN_MENU}", reply_markup=main_menu)
