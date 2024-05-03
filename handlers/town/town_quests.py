from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

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
      loc_quests = ['q_1', 'q_2', 'q_3', 'q_4']
      text = 'Вы заходите в ратушу'
      
      cur.execute(f"SELECT active FROM quests WHERE id_tg = %s", [callback.message.chat.id])
      res = cur.fetchone()[0]
      if res:
         flag = True
         for quest in res:
            if quest in loc_quests:
               builder.row(InlineKeyboardButton(text=f'+ {quests[quest]["name"]} +', callback_data=f'{quest}-info-active'))
               
      cur.execute(f"SELECT open FROM quests WHERE id_tg = %s", [callback.message.chat.id])
      res = cur.fetchone()[0]
      if res:
         flag = True
         for quest in res:
            if quest in loc_quests:
               builder.row(InlineKeyboardButton(text=quests[quest]['name'], callback_data=f'{quest}-info'))
      
      # for index, quest in enumerate(quests[:4], start=1):
      #    cur.execute(f"SELECT q_{index} FROM quests WHERE id_tg = %s", [callback.message.chat.id])
      #    res = cur.fetchone()[0]
      #    if res == 'open':
      #       flag = True
      #       builder.row(InlineKeyboardButton(text=quest['name'], callback_data=f'q_{index}_info'))
      #    elif res == 'active':
      #       flag = True
      #       builder.row(InlineKeyboardButton(text=f"{quest['name']} ☑️", callback_data=f'q_{index}_info-active'))
         

   cur.close()
   conn.close()
   builder.row(InlineKeyboardButton(text='Назад', callback_data='town'))

   if not flag:
      text = 'Сейчас поручений нет'
      
   await callback.message.edit_text(text=text, reply_markup=builder.as_markup())
   
@router.callback_query(F.data.endswith('-info'))
async def f(callback: CallbackQuery):
   quest_ind = callback.data.split('-')[0]
   name = quests[quest_ind]['name']
   text = quests[quest_ind]['text']
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Принять', callback_data=f'{quest_ind}-active'))
   builder.row(InlineKeyboardButton(text='Назад', callback_data='quests'))
   
   await callback.message.edit_text(text=f'<b>{name}</b> \n\n {text}', reply_markup=builder.as_markup(), parse_mode='HTML')
   
@router.callback_query(F.data.endswith('-info-active'))
async def f(callback: CallbackQuery):
   quest_ind = callback.data.split('-')[0]
   name = quests[quest_ind]['name']
   text = quests[quest_ind]['text']
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Не отслеживать', callback_data=f'{quest_ind}-diactive'))
   builder.row(InlineKeyboardButton(text='Назад', callback_data='quests'))
   
   await callback.message.edit_text(text=f'<b>{name}</b> \n\n {text}', reply_markup=builder.as_markup(), parse_mode='HTML')
   

@router.callback_query(F.data.endswith('-active'))
async def f(callback: CallbackQuery):
   quest_ind = callback.data.split('-')[0]
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   
   # cur.execute(f"UPDATE quests SET q_{quest_num} = 'active' WHERE id_tg=%s", [callback.message.chat.id])
   cur.execute(f"UPDATE quests SET active = active || %s WHERE id_tg = %s", ([quest_ind], callback.message.chat.id))
   cur.execute(f"UPDATE quests SET open = array_remove(open, %s) WHERE id_tg = %s", (quest_ind, callback.message.chat.id))
   
   conn.commit()
   cur.close()
   conn.close()
   
   await func_quests(callback)

@router.callback_query(F.data.endswith('-diactive'))
async def f(callback: CallbackQuery):
   quest_ind = callback.data.split('-')[0]
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   
   # cur.execute(f"UPDATE quests SET q_{quest_num} = 'open' WHERE id_tg=%s", [callback.message.chat.id])
   cur.execute(f"UPDATE quests SET open = open || %s WHERE id_tg = %s", ([quest_ind], callback.message.chat.id))
   cur.execute(f"UPDATE quests SET active = array_remove(active, %s) WHERE id_tg = %s", (quest_ind, callback.message.chat.id))
   
   conn.commit()
   cur.close()
   conn.close()
   
   await func_quests(callback)