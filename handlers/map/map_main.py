from asyncio import sleep, Event, create_task
from aiogram import Router, F
import aiogram
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from random import randint
from math import ceil
from apps.transition_events.events_main import transitionEvent
from apps.transition_events.events_content import event_1, event_2

router = Router()

cancel_event = Event()

async def cbd_map(callback):
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
   builder.row(InlineKeyboardButton(text=f'{now_location.title()} <- вы здесь', callback_data='#'))

   if now_location == 'Эвертон':
      photo = FSInputFile('Base/data/images/map_tiles/everton.jpg')

      builder.row(InlineKeyboardButton(text='Имение Чапси', callback_data='имение Чапси'))
      builder.row(InlineKeyboardButton(text='Амбербрук', callback_data='Амбербрук'))
   elif now_location == 'Амбербрук':
      photo = FSInputFile('Base/data/images/map_tiles/everton.jpg')

      builder.row(InlineKeyboardButton(text='Эвертон', callback_data='Эвертон'))
      cur.execute(f'SELECT Copper FROM users_map WHERE id_tg = %s', [callback.message.chat.id])
      if cur.fetchone()[0] == 1:
         builder.row(InlineKeyboardButton(text='Коппер', callback_data='Коппер'))
   elif now_location == 'имение Чапси':
      photo = FSInputFile('Base/data/images/map_tiles/everton.jpg')

      builder.row(InlineKeyboardButton(text='Эвертон', callback_data='Эвертон'))
      cur.execute(f'SELECT Emberwood FROM users_map WHERE id_tg = %s', [callback.message.chat.id])
      if cur.fetchone()[0] == 1:
         builder.row(InlineKeyboardButton(text='Эмбервуд', callback_data='Эмбервуд'))

   # Окрестности
   elif now_location == 'лесопилка Доппи':
      photo = FSInputFile('Base/data/images/map_tiles/environs/everton_environs.jpg') # нужно заменить фотки
   elif now_location == 'тестовая локация':
      photo = FSInputFile('Base/data/images/map_tiles/environs/amberbrook_environs.jpg')

   else:
      photo = FSInputFile('Base/data/images/white.png')

   cur.close()
   conn.close()

   if now_location not in ['лесопилка Доппи', 'тестовая локация']:
      builder.row(InlineKeyboardButton(text='Окрестности', callback_data='environs'))
   else:
      if now_location in ['лесопилка Доппи']:
         cb_city = 'Эвертон' # можно посмотреть в map_environs
      elif now_location in ['тестовая локация']:
         cb_city = 'Амбербрук'
      builder.row(InlineKeyboardButton(text='Покинуть окрестности', callback_data=cb_city))
      
   builder.row(InlineKeyboardButton(text='Назад', callback_data='menu'))

   await callback.message.delete()
   await sleep(0.75)
   await callback.message.answer_photo(photo=photo, caption='Вы открываете карту. Куда отправимся?', reply_markup=builder.as_markup())

async def transition(callback, distance, name, type='city', subname=None):
   await callback.answer('Движемся...')
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Отменить путешествие', callback_data='transition_cancel'))

   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   cur.execute(f'SELECT speed FROM users WHERE id_tg = %s', [callback.message.chat.id])
   speed = cur.fetchone()[0]
   cur.close()
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
      if i == time_to_check_event and type == 'city':
         await transitionEvent(callback=callback, chance=0.1)
      if cancel_event.is_set():
         flag_transiton = False
         break
      
      if type == 'city':
         new_text = f'Вы направляетесь в {name}. {text}'
      else:
         new_text = f'Вы направляетесь в окрестность "{subname}". {text}'
      new_markup = builder.as_markup()
      
      if new_text != callback.message.text or new_markup != callback.message.reply_markup:
         try:
            await callback.message.edit_caption(caption=new_text, reply_markup=new_markup)
         except aiogram.exceptions.TelegramBadRequest:
            pass

      await sleep(1)
   
   if flag_transiton:
      conn = psycopg2.connect(
         host=host,
         user=user,
         password=password,
         database=db_name
      )
      cur = conn.cursor()

      if type == 'city':
         cur.execute(f'UPDATE users_map SET now_location = %s WHERE id_tg=%s', [name, callback.message.chat.id,])
      else:
         cur.execute(f'UPDATE users_map SET now_location = %s WHERE id_tg=%s', [subname, callback.message.chat.id,])

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
         if type == 'city':
            await callback.message.edit_caption(caption=f'Путешествие в {name} завершено', reply_markup=builder.as_markup())
         else:
            await callback.message.edit_caption(caption=f'Путешествие в окрестность "{subname}" завершено', reply_markup=builder.as_markup())

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