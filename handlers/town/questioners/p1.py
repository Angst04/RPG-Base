# Арнольд
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, FSInputFile, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

router = Router()

@router.callback_query(F.data == 'p1')
async def f(callback: CallbackQuery):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   builder = InlineKeyboardBuilder()

   cur.execute(f'SELECT p1_1 FROM quests WHERE id_tg = %s', [callback.message.chat.id])
   res = cur.fetchone()[0]
   if res == 'open':
      builder.row(InlineKeyboardButton(text='Рубка леса', callback_data='p1_1'))
   elif res == 'active':
      builder.row(InlineKeyboardButton(text='Рубка леса ☑️', callback_data='p1_1'))
   elif res == 'complete':
      builder.row(InlineKeyboardButton(text='Рубка леса ☑️☑️☑️', callback_data='#'))
      
   cur.execute(f'SELECT p1_2 FROM quests WHERE id_tg = %s', [callback.message.chat.id])
   res = cur.fetchone()[0]
   if res == 'open':
      builder.row(InlineKeyboardButton(text='Зачистка лагеря', callback_data='p1_2'))
   elif res == 'active':
      builder.row(InlineKeyboardButton(text='Зачистка лагеря ☑️', callback_data='p1_2'))
   elif res == 'complete':
      builder.row(InlineKeyboardButton(text='Зачистка лагеря ☑️☑️☑️', callback_data='#'))
   
   cur.close()
   conn.close()
   
   builder.row(InlineKeyboardButton(text='Назад', callback_data='quests'))
   
   await callback.message.edit_text(text='Арнольд достаёт пыльную стопку бумаг и принимается читать', reply_markup=builder.as_markup())
      
@router.callback_query(F.data == 'p1_1')
async def f(callback: CallbackQuery):
   builder = InlineKeyboardBuilder()
   
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT p1_1 FROM quests WHERE id_tg = %s', [callback.message.chat.id])
   
   if cur.fetchone()[0] != 'active':
      builder.row(InlineKeyboardButton(text='Принять', callback_data='p1_1_active'))
      
   builder.row(InlineKeyboardButton(text='Назад', callback_data='p1'))
   
   await callback.message.edit_text(text='Отправляйся ка ты в лес и принеси мне дров', reply_markup=builder.as_markup())
   
@router.callback_query(F.data == 'p1_1_active')
async def f(callback: CallbackQuery):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f"UPDATE quests SET p1_1 = 'active' WHERE id_tg=%s", [callback.message.chat.id])
   conn.commit()
   cur.close()
   conn.close()
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Назад', callback_data='p1'))
   await callback.answer(text='Задание принято ☑️', show_alert=True)
   await callback.message.edit_text(text='Отправляйся ка ты в лес и принеси мне дров', reply_markup=builder.as_markup())