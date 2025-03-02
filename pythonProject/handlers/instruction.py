from aiogram import Router, F
from aiogram.types import CallbackQuery

from keybords import back_to_main_menu
from bot.messages import INSTRUCTION

instruction_router = Router()

@instruction_router.callback_query(F.data == 'instruction')
async def instruction_button(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(INSTRUCTION, reply_markup=back_to_main_menu)