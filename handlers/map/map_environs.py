from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import sqlite3
#from core.keyboards import kb_map

router = Router()

@router.callback_query(F.data == 'Лесопилка_Доппи')
async def f(callback: CallbackQuery):
   builder = InlineKeyboardBuilder()

   builder.row(InlineKeyboardButton(text='Осмотреть', callback_data='#'))
   builder.row(InlineKeyboardButton(text='Вернуться', callback_data='map'))

   await callback.message.edit_text(text='Вы находитесь на лесопилке Доппи', reply_markup=builder.as_markup())