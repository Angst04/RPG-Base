from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.callback_query(F.data == 'AC1')
async def AC1(callback: CallbackQuery):
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Назад', callback_data='achievements'))
   await callback.message.edit_text(text='Описание 1 достижения', reply_markup=builder.as_markup())