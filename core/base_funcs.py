from aiogram.types import FSInputFile

import json
import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

# функция для получения достижения
async def get_ac(callback, ac_name):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   

   cur.execute(f'SELECT "{ac_name}" FROM achievements WHERE id_tg = %s', [callback.message.chat.id])
   if cur.fetchone()[0] != 1:
      await callback.answer(text=f'Получено достижение!\n\n{ac_name}', show_alert=True)

   cur.execute(f'UPDATE achievements SET "{ac_name}" = 1 WHERE id_tg=%s', [callback.message.chat.id])

   conn.commit()
   cur.close()
   conn.close()
   

# функция для создания индикатора hp
async def health_ind(amount, builder):
   n = amount
   
   tens_count = amount // 10
   amount %= 10
   fives_count = amount // 5
   amount %= 5
   
   builder.button(text='HP:', callback_data='info_hp')
   
   if tens_count + fives_count + amount >= 5:
      builder.button(text=f'❤️×{n}', callback_data='info_hp')

   else:
      for _ in range(tens_count):
         builder.button(text='❤️×10', callback_data='info_hp')
         
      for _ in range(fives_count):
         builder.button(text='❤️×5', callback_data='info_hp')

      for _ in range(amount):
         builder.button(text='❤️', callback_data='info_hp')
      
   return builder


# функции для изменения и получения состояния занятости
async def busy_change(chat_id, status):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   if status:
      cur.execute(f'UPDATE users SET busy = 1 WHERE id_tg=%s', [chat_id])
   else:
      cur.execute(f'UPDATE users SET busy = 0 WHERE id_tg=%s', [chat_id])
   conn.commit()
   cur.close()
   conn.close()
   
async def busy_check(message):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT busy FROM users WHERE id_tg=%s', [message.chat.id])
   res = cur.fetchone()[0]
   cur.close()
   conn.close()
   if res == 1:
      return True
   return False


async def get_card(callback, card_id):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'UPDATE collections SET "{card_id}" = 1 WHERE id_tg=%s', [callback.message.chat.id])
   conn.commit()
   cur.close()
   conn.close()
   
   with open('./data/cards.json', 'r') as file:
      card_data = json.load(file)
   
   for card in card_data['cards']:
         if card['id'] == card_id:
            title = card['title']
            
   await callback.answer(text=f'Получена новая карта!\n\n{title}', show_alert=True)
   

async def check_menu_id(callback):
   conn = psycopg2.connect(
         host=host,
         user=user,
         password=password,
         database=db_name
      )
   cur = conn.cursor()
   cur.execute(f'SELECT menu_id FROM users WHERE id_tg = %s', [callback.message.chat.id])
   res = cur.fetchone()[0]
   conn.close()
   cur.close()   
   if callback.message.message_id == res:
      return True
   else:
      await callback.answer(text='Данное меню не актуально\nВоспользуйтесь командой\n/menu', show_alert=True)
      return False