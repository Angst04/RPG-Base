from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from asyncio import create_task, sleep
from core.dbs_config import host, user, password, db_name
from .map_main import transition, cancel_event

router = Router()

async def cbd_environs(callback):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   builder = InlineKeyboardBuilder()

   cur.execute(f'SELECT now_location FROM users_map WHERE id_tg = %s', [callback.message.chat.id])
   now_location = cur.fetchone()[0]
   flag = False
   cur.close()
   conn.close()

   if now_location == 'Эвертон':
      flag = True
      builder.row(InlineKeyboardButton(text='Лесопилка Доппи', callback_data='лесопилка Доппи'))
      photo = FSInputFile('Base/data/images/map_tiles/environs/everton_environs.jpg')

   elif now_location == 'Амбербрук':
      flag = True
      builder.row(InlineKeyboardButton(text='Тестовая локация', callback_data='тестовая локация'))
      photo = FSInputFile('Base/data/images/map_tiles/environs/amberbrook_environs.jpg')

   builder.row(InlineKeyboardButton(text='Назад', callback_data='map'))

   if flag:
      await callback.message.delete()
      await sleep(0.75)
      await callback.message.answer_photo(photo=photo, caption='Посморим-ка на окрестности... Куда отправимся?', reply_markup=builder.as_markup())
   else:
      await callback.message.edit_caption(caption='В окрестностях ничего нет', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'лесопилка Доппи')
async def f(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Эвертон', 'environs', 'лесопилка Доппи'))

@router.callback_query(F.data == 'тестовая локация')
async def f(callback: CallbackQuery):
   global cancel_event
   cancel_event.clear()
   create_task(transition(callback, 1, 'Амбербрук', 'environs', 'тестовая локация'))