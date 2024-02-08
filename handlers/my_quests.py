from aiogram import Router
from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

async def cbd_quests(callback):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   # cur.execute(f'SELECT now_location FROM users_map WHERE id_tg = %s', [callback.message.chat.id])
   # now_location = cur.fetchone()[0]
   cur.close()
   conn.close()
   
   builder = InlineKeyboardBuilder()
   
   builder.row(InlineKeyboardButton(text='Назад', callback_data='menu'))
   
   await callback.message.edit_text(text='Список ваших поручений:', reply_markup=builder.as_markup())