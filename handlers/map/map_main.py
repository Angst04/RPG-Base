from asyncio import sleep, Event, create_task
from aiogram import Router, F
import aiogram
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import sqlite3
from random import randint
from math import ceil
from apps.transition_events.events_main import transitionEvent
from apps.transition_events.events_content import event_1, event_2

router = Router()

cancel_event = Event()

async def transition(callback, distance, name, type='city', subname=None):
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
   try:
      time_to_check_event = randint(10, time - 1)
   except ValueError:
      time_to_check_event = 9999

   for i in range(int(time)):
      if i == time_to_check_event:
         await transitionEvent(callback=callback, chance=0.25)
      if cancel_event.is_set():
         flag_transiton = False
         break
      
      if type == 'city':
         new_text = f'Вы направляетесь в {name}. {text}'
      else:
         new_text = f'Вы направляетесь в {subname}. {text}'
      new_markup = builder.as_markup()
      
      if new_text != callback.message.text or new_markup != callback.message.reply_markup:
         try:
            await callback.message.edit_caption(caption=new_text, reply_markup=new_markup)
         except aiogram.exceptions.TelegramBadRequest:
            pass

      await sleep(1)
   
   if flag_transiton:
      conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
      cur = conn.cursor()
      if type == 'city':
         cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', (name, callback.message.chat.id,))
      else:
         cur.execute('UPDATE users_map SET now_location = ? WHERE id_tg=?', (subname, callback.message.chat.id,))

      builder = InlineKeyboardBuilder()
      if type == 'city':
         builder.row(InlineKeyboardButton(text='Продолжить путь', callback_data='map'))
      else:
         builder.row(InlineKeyboardButton(text='Покинуть окрестности', callback_data=f'{name}'))
      builder.row(InlineKeyboardButton(text='Остаться', callback_data='menu'))
      
      conn.commit()
      cur.close()
      conn.close()

      try:
         await callback.message.edit_caption(caption=f'Путешествие в {name} завершено', reply_markup=builder.as_markup())
      except aiogram.exceptions.TelegramBadRequest:
         pass


@router.callback_query(F.data == 'transition_cancel')
async def cancelTransition(callback: CallbackQuery):
   global cancel_event
   cancel_event.set()

   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Вернуться к карте', callback_data='map'))

   await callback.message.delete()
   await callback.message.answer(text='Путешествие отменено', reply_markup=builder.as_markup())


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

router.include_routers(event_1.router, event_2.router)