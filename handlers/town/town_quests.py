from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name
from data.quests_desc import quests

router = Router()

@router.callback_query(F.data == 'quests')
async def func_quests(callback: CallbackQuery):
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
            builder.row(InlineKeyboardButton(text=f"{quest['name']} ☑️", callback_data=f'q_{index}_info-active'))
         

   cur.close()
   conn.close()
   builder.row(InlineKeyboardButton(text='Назад', callback_data='town'))

   if not flag:
      text = 'Сейчас поручений нет'
      
   await callback.message.edit_text(text=text, reply_markup=builder.as_markup())
   
@router.callback_query(F.data.endswith('_info'))
async def f(callback: CallbackQuery):
   quest_num = int(callback.data.split('_')[1])
   name = quests[quest_num - 1]['name']
   text = quests[quest_num - 1]['text']
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Принять', callback_data=f'q_{quest_num}_active'))
   builder.row(InlineKeyboardButton(text='Назад', callback_data='quests'))
   
   await callback.message.edit_text(text=f'<b>{name}</b> \n\n {text}', reply_markup=builder.as_markup(), parse_mode='HTML')
   
@router.callback_query(F.data.endswith('_info-active'))
async def f(callback: CallbackQuery):
   quest_num = int(callback.data.split('_')[1])
   name = quests[quest_num - 1]['name']
   text = quests[quest_num - 1]['text']
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Не отслеживать', callback_data=f'q_{quest_num}_diactive'))
   builder.row(InlineKeyboardButton(text='Назад', callback_data='quests'))
   
   await callback.message.edit_text(text=f'<b>{name}</b> \n\n {text}', reply_markup=builder.as_markup(), parse_mode='HTML')
   

@router.callback_query(F.data.endswith('_active'))
async def f(callback: CallbackQuery):
   quest_num = int(callback.data.split('_')[1])
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   
   cur.execute(f"UPDATE quests SET q_{quest_num} = 'active' WHERE id_tg=%s", [callback.message.chat.id])
   
   conn.commit()
   cur.close()
   conn.close()
   
   await func_quests(callback)

@router.callback_query(F.data.endswith('_diactive'))
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
   
   await func_quests(callback)