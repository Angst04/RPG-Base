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
   conn.close()

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
         flag_transiton = False
         break

      new_text = f'Вы направляетесь в {name.title()}. {text}'
      new_markup = builder.as_markup()

      
      if new_text != callback.message.text or new_markup != callback.message.reply_markup:
         try:
            await callback.message.edit_text(text=new_text, reply_markup=new_markup)
         except aiogram.exceptions.TelegramBadRequest:
            pass

      await sleep(1)
   
   if flag_transiton:
      builder = InlineKeyboardBuilder()
      builder.row(InlineKeyboardButton(text='Продолжить путь', callback_data='map'))
      builder.row(InlineKeyboardButton(text='Остаться', callback_data='menu'))

      conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
      cur = conn.cursor()   
      cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', (name, callback.message.chat.id,))
      conn.commit()
      cur.close()
      conn.close()

      await callback.message.edit_text(text=f'Путешествие в {name.title()} завершено', reply_markup=builder.as_markup())
      await callback.message.edit_caption(caption='Base/data/images/map_tiles/all_map.png')


@router.callback_query(F.data == 'transition_cancel')
async def cancel_transition(callback: CallbackQuery):
   global cancel_event
   cancel_event.set()

   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Вернуться к карте', callback_data='map'))

   await callback.message.edit_text(text='Путешествие отменено', reply_markup=builder.as_markup())
   await callback.message.edit_caption(caption='Base/data/images/map_tiles/all_map.png')


@router.callback_query(F.data == 'имение Чапси')
async def func(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'имение Чапси'))

@router.callback_query(F.data == 'Амбербрук')
async def func(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Амбербрук'))

@router.callback_query(F.data == 'Эвертон')
async def func(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Эвертон'))

@router.callback_query(F.data == 'Коппер')
async def func(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Коппер'))