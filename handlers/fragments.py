from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

async def cbd_fragments(callback):
   builder = InlineKeyboardBuilder()
   
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   
   name = 'Ярость бури'
   cur.execute(f'SELECT "{name}" FROM fragments WHERE id_tg = %s', [callback.message.chat.id])
   count = cur.fetchone()[0]
   if count != -1:
      builder.row(InlineKeyboardButton(text=f'{name} {count}/4', callback_data='#'))

      
   name = 'Вознесение'
   cur.execute(f'SELECT "{name}" FROM fragments WHERE id_tg = %s', [callback.message.chat.id])
   count = cur.fetchone()[0]
   if count != -1:
      builder.row(InlineKeyboardButton(text=f'{name} {count}/4', callback_data='#'))
   
   name = 'Скрытый талант'
   cur.execute(f'SELECT "{name}" FROM fragments WHERE id_tg = %s', [callback.message.chat.id])
   count = cur.fetchone()[0]
   if count != -1:
      builder.row(InlineKeyboardButton(text=f'{name} {count}/4', callback_data='#'))
      
   cur.close()
   conn.close()
   
   builder.row(InlineKeyboardButton(text='Назад', callback_data='menu_other'))
   
   await callback.message.edit_text(text='Список собранных фрагментов:', reply_markup=builder.as_markup())
   
async def raise_fragment(callback, name):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   
   cur.execute(f'SELECT "{name}" FROM fragments WHERE id_tg = %s', [callback.message.chat.id])
   count = cur.fetchone()[0]
   if count != -1:
      count += 1
      if count == 4:
         await callback.answer(text=f'Получена новая карта!\n\n{name}', show_alert=True)
         cur.execute(f'UPDATE fragments SET "{name}" = -1 WHERE id_tg=%s', [callback.message.chat.id])
         cur.execute(f'UPDATE collections SET c_0004 = 1 WHERE id_tg=%s', [callback.message.chat.id])
         conn.commit()
      elif 0 <= count <= 3:
         await callback.answer(text=f'Получен фрагмент карты\n\n{name}', show_alert=True)
         cur.execute(f'UPDATE fragments SET "{name}" = {count} WHERE id_tg=%s', [callback.message.chat.id])
         conn.commit()
   
   cur.close()
   conn.close()