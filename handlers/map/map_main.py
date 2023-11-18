#import asyncio
from asyncio import sleep, Event, create_task
from aiogram import Router, F
import aiogram
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import sqlite3
from math import ceil
from core.keyboards import kb_map
#from handlers.map.map_func import transition

router = Router()

cancel_event = Event()

async def transition(callback, distance, name):
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Отменить путешествие', callback_data='transition_cancel'))

   conn = sqlite3.connect('Base/data/users.sql', check_same_thread=False)

   speed = conn.execute(f'SELECT speed FROM users WHERE id_tg = {callback.message.chat.id}').fetchone()[0]
   time = distance / speed * 60

   if time < 60:
      text = 'Время в пути меньше минуты'
   elif 60 <= time < 120:
      text = 'Время в пути около минуты'
   else:
      text = f'Время в пути около {ceil(time / 60)} минут'

   flag_transiton = True
   for _ in range(int(time)):
      if cancel_event.is_set():
         text += '\n\nПутешествие отменено.'
         flag_transiton = False
         break

      new_text = f'Вы направляетесь в {name}. {text}'
      new_markup = builder.as_markup()

      
      if new_text != callback.message.text or new_markup != callback.message.reply_markup:
         try:
            await callback.message.edit_text(text=new_text, reply_markup=new_markup)
         except aiogram.exceptions.TelegramBadRequest as e:
            pass

      await sleep(1)
   
   if flag_transiton:
      await callback.message.edit_text(text=f'Путешествие в {name} завершено.', reply_markup=None)


transition_flag = False
@router.callback_query(F.data == 'transition_cancel')
async def cancel_transition(callback: CallbackQuery):
   global cancel_event
   cancel_event.set()
   global transition_flag
   transition_flag = False

   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Вернуться к карте', callback_data='map'))

   await callback.message.edit_text(text='Перемещение отменено', reply_markup=builder.as_markup())


@router.callback_query(F.data == 'Имениe_Чапси')
async def func(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Имениe Чапси'))

   global transition_flag

   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   if transition_flag != False:
      cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', ('Имениe_Чапси', callback.message.chat.id,))
      conn.commit()
      cur.close()
      conn.close()

   await callback.message.edit_text(text='Вы находитесь в имении Чапси', reply_markup=kb_map)

@router.callback_query(F.data == 'Амбербрук')
async def func(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Амбербрук'))

   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   if transition_flag != False:
      cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', ('Амбербрук', callback.message.chat.id,))
      conn.commit()
      cur.close()
      conn.close()

   await callback.message.edit_text(text='Вы находитесь в Амбербруке', reply_markup=kb_map)

@router.callback_query(F.data == 'Эвертон')
async def func(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Эвертон'))

   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   if transition_flag != False:
      cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', ('Эвертон', callback.message.chat.id,))
      conn.commit()
      cur.close()
      conn.close()

   await callback.message.edit_text(text='Вы находитесь в Эвертоне', reply_markup=kb_map)

@router.callback_query(F.data == 'Коппер')
async def func(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Коппер'))
   
   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   if transition_flag != False:
      cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', ('Коппер', callback.message.chat.id,))
      conn.commit()
      cur.close()
      conn.close()

   await callback.message.edit_text(text='Вы находитесь в Коппере', reply_markup=kb_map)