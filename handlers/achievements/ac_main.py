from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

async def cbd_achievements(callback):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   builder = InlineKeyboardBuilder()
   k = 0

   cur.execute(f'SELECT a1 FROM achievements WHERE id_tg = %s', [callback.message.chat.id])
   if cur.fetchone()[0] == 1:
      builder.row(InlineKeyboardButton(text='Серьёзный выбор', callback_data='AC1'))
      k += 1
   cur.execute(f'SELECT a2 FROM achievements WHERE id_tg = %s', [callback.message.chat.id])
   if cur.fetchone()[0] == 1:
      builder.row(InlineKeyboardButton('Не менее серьёзный выбор', callback_data='AC2'))
      k += 1

   builder.row(InlineKeyboardButton(text='Назад', callback_data='menu_other'))
   if k > 0:
      await callback.message.edit_text(text='Ваши достижения', reply_markup=builder.as_markup())
   elif k == 0:
      await callback.message.edit_text(text='Здесь ничего нет(', reply_markup=builder.as_markup())

   cur.close()
   conn.close()