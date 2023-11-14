from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import sqlite3
from core.keyboards import kb_map

router = Router()

@router.callback_query(F.data == 'Имениe_Чапси')
async def func(callback: CallbackQuery):
   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', ('Имениe_Чапси', callback.message.chat.id,))
   conn.commit()
   cur.close()
   conn.close()

   await callback.message.edit_text(text='Вы находитесь в имении Чапси', reply_markup=kb_map)

@router.callback_query(F.data == 'Амбербрук')
async def func(callback: CallbackQuery):
   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', ('Амбербрук', callback.message.chat.id,))
   conn.commit()
   cur.close()
   conn.close()

   await callback.message.edit_text(text='Вы находитесь в Амбербруке', reply_markup=kb_map)

@router.callback_query(F.data == 'Эвертон')
async def func(callback: CallbackQuery):
   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', ('Эвертон', callback.message.chat.id,))
   conn.commit()
   cur.close()
   conn.close()

   await callback.message.edit_text(text='Вы находитесь в Эвертоне', reply_markup=kb_map)

@router.callback_query(F.data == 'Коппер')
async def func(callback: CallbackQuery):
   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', ('Коппер', callback.message.chat.id,))
   conn.commit()
   cur.close()
   conn.close()

   await callback.message.edit_text(text='Вы находитесь в Коппере', reply_markup=kb_map)