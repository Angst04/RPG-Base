from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.keyboards import menu

router = Router()

@router.callback_query(F.data == 'achievements')
async def cbd_achievements(callback: CallbackQuery):
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(
      text='Назад', callback_data='menu'
   ))
   await callback.message.edit_text(text='Ваши достижения', reply_markup=builder.as_markup())