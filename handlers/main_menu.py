from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.keyboards import kb_menu
import sqlite3

router = Router()

@router.callback_query(F.data == 'achievements')
async def cbd_achievements(callback: CallbackQuery):
   conn = sqlite3.connect('Base/data/achievements.sql', check_same_thread=False)

   builder = InlineKeyboardBuilder()
   k = 0

   if conn.execute(f'SELECT a1 FROM achievements WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 1:
      builder.row(InlineKeyboardButton(text='Серьёзный выбор', callback_data='AC1'))
      k += 1
   if conn.execute(f'SELECT a2 FROM achievements WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 1:
      builder.row(InlineKeyboardButton('Не менее серьёзный выбор', callback_data='AC2'))
      k += 1

   builder.row(InlineKeyboardButton(text='Назад', callback_data='menu'))
   if k > 0:
      await callback.message.edit_text(text='Ваши достижения', reply_markup=builder.as_markup())
   elif k == 0:
      await callback.message.edit_text(text='Здесь ничего нет(', reply_markup=builder.as_markup())

   conn.close()