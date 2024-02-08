from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name
from data.quests_desc import quests

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
      
      for index, quest in enumerate(quests[:4], start=1):
         cur.execute(f"SELECT q_{index} FROM quests WHERE id_tg = %s", [callback.message.chat.id])
         res = cur.fetchone()[0]
         if res == 'open':
            flag = True
            builder.row(InlineKeyboardButton(text=quest['name'], callback_data=f'q_{index}_info'))
         elif res == 'active':
            flag = True
            builder.row(InlineKeyboardButton(text=f"{quest['name']} ☑️", callback_data=f'q_{index}_info'))
         

   cur.close()
   conn.close()
   builder.row(InlineKeyboardButton(text='Назад', callback_data='town'))

   if not flag:
      text = 'Сейчас поручений нет'
      
   await callback.message.edit_text(text=text, reply_markup=builder.as_markup())