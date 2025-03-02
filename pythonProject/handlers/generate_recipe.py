from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from bot.messages import GENERATE_OBJECT, GENERATED_BY_NAME
from keybords import generate_object
from states import GenerateObject

generate_recipe_router = Router()

@generate_recipe_router.callback_query(F.data == 'generate_recipe')
async def choose_generate_object(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(GENERATE_OBJECT, reply_markup=generate_object)

@generate_recipe_router.callback_query(F.data == 'generate_name')
async def get_name_by_generated(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(GENERATED_BY_NAME)
    await state.set_state(GenerateObject.name)



