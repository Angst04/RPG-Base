from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from handlers.town.questioners import p1, p2

router = Router()

@router.callback_query(F.data == 'quests')
async def f(callback: CallbackQuery):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT now_location FROM users_map WHERE id_tg = %s', [callback.message.chat.id])
   now_location = cur.fetchone()[0]
   
   builder = InlineKeyboardBuilder()
   
   flag = False
   if now_location == 'Эвертон':
      text = 'Вы заходите в ратушу'
      
      cur.execute(f"SELECT 'open' FROM quests WHERE id_tg = %s AND ('open' IN (p1_1, p1_2, p1_3, p1_4))", [callback.message.chat.id])
      if cur.fetchone():
         builder.row(InlineKeyboardButton(text='Арнольд', callback_data='p1'))
         flag = True

      cur.execute(f"SELECT 'open' FROM quests WHERE id_tg = %s AND ('open' IN (p2_1, p2_2))", [callback.message.chat.id])
      if cur.fetchone():
         builder.row(InlineKeyboardButton(text='Бади', callback_data='p2'))
         flag = True

   cur.close()
   conn.close()
   builder.row(InlineKeyboardButton(text='Назад', callback_data='town'))

   if not flag:
      text = 'Сейчас поручений нет'
   else:
      await callback.message.edit_text(text=text, reply_markup=builder.as_markup())

router.include_routers(p1.router, p2.router)