from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

from data.quests_desc import quests

router = Router()

@router.callback_query(F.data.endswith('my_quests'))
async def cbd_quests(callback):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   
   builder = InlineKeyboardBuilder()

   flag = False
   for i in range(1, 7):
      cur.execute(f"SELECT q_{i} FROM quests WHERE id_tg = %s", [callback.message.chat.id])
      res = cur.fetchone()[0]
      if res == 'active':
         flag = True
         name = quests[i - 1]["name"]
         builder.row(InlineKeyboardButton(text=name, callback_data=f'q_{i}_info-my'))

   cur.close()
   conn.close()
   
   builder.row(InlineKeyboardButton(text='Главное меню', callback_data='menu'))

   if flag:
      text = 'Список ваших поручений:'
   else:
      text = 'У вас нет активных поручений'
      
   await callback.message.edit_text(text=text, reply_markup=builder.as_markup())
   

@router.callback_query(F.data.endswith('_info-my'))
async def f(callback: CallbackQuery):
   quest_num = int(callback.data.split('_')[1])
   name = quests[quest_num - 1]['name']
   text = quests[quest_num - 1]['text']
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Не отслеживать', callback_data=f'q_{quest_num}_diactive-my'))
   builder.row(InlineKeyboardButton(text='Назад', callback_data='my_quests'))
   
   await callback.message.edit_text(text=f'<b>{name}</b> \n\n {text}', reply_markup=builder.as_markup(), parse_mode='HTML')
   
   
@router.callback_query(F.data.endswith('_diactive-my'))
async def f(callback: CallbackQuery):
   quest_num = int(callback.data.split('_')[1])
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   
   cur.execute(f"UPDATE quests SET q_{quest_num} = 'open' WHERE id_tg=%s", [callback.message.chat.id])
   
   conn.commit()
   cur.close()
   conn.close()
   
   await cbd_quests(callback)