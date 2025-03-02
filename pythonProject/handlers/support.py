from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


from states import TechnicalSupport as ts
from keybords import main_menu
from bot.messages import SUPPORT, MAIN_MENU
from bot import ADMIN_ID

support_router = Router()

@support_router.callback_query(F.data == 'technical_support')
async def technical_support_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ts.mes)
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(SUPPORT)

@support_router.message(ts.mes)
async def complete_send_technical_support_message(message: Message, state: FSMContext):
    await message.answer(f'Сообщение: {message.text} успешно отправлено!')
    await message.bot.send_message(ADMIN_ID,
                                   f'ID: {message.from_user.id}\nИмя: {message.from_user.first_name}\n Сообщение: {message.text}')
    await message.answer(MAIN_MENU, reply_markup=main_menu)
    await state.clear()