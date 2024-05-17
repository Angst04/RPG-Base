from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

async def cbd_hero(callback):
   builder = InlineKeyboardBuilder()
   
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   
   cur.execute(f'SELECT health FROM users WHERE id_tg = %s', [callback.message.chat.id])
   health = cur.fetchone()[0]
   cur.execute(f'SELECT speed FROM users WHERE id_tg = %s', [callback.message.chat.id])
   speed = cur.fetchone()[0]
   cur.execute(f'SELECT money FROM users WHERE id_tg = %s', [callback.message.chat.id])
   money = cur.fetchone()[0]
   cur.close()
   conn.close()
   
   builder.row(InlineKeyboardButton(text='Назад', callback_data='menu_other'))
   
   await callback.message.edit_text(
      text='<b>Информация о вашем герое</b>\n\n'
      f'<b>Здоровье:</b> {health}\n'
      f'<b>Скорость передвижения:</b> {speed}\n'
      f'<b>Лумены:</b> {money}',
      
      reply_markup=builder.as_markup(), 
      parse_mode='HTML'
   )