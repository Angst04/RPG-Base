from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from handlers.map import map_main, map_environs

router = Router()

@router.callback_query(F.data == 'achievements')
async def cbd_achievements(callback: CallbackQuery):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   builder = InlineKeyboardBuilder()
   k = 0

   cur.execute(f'SELECT a1 FROM achievements WHERE id_tg = %s', [callback.message.chat.id])
   if cur.fetchone()[0] == 1:
      builder.row(InlineKeyboardButton(text='Серьёзный выбор', callback_data='AC1'))
      k += 1
   cur.execute(f'SELECT a2 FROM achievements WHERE id_tg = %s', [callback.message.chat.id])
   if cur.fetchone()[0] == 1:
      builder.row(InlineKeyboardButton('Не менее серьёзный выбор', callback_data='AC2'))
      k += 1

   builder.row(InlineKeyboardButton(text='Назад', callback_data='menu_other'))
   if k > 0:
      await callback.message.edit_text(text='Ваши достижения', reply_markup=builder.as_markup())
   elif k == 0:
      await callback.message.edit_text(text='Здесь ничего нет(', reply_markup=builder.as_markup())

   cur.close()
   conn.close()


@router.callback_query(F.data == 'map')
async def cbd_map(callback: CallbackQuery):
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
   await callback.message.answer_photo(photo=photo, caption='Вы открываете карту. Куда отправимся?', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'environs')
async def f(callback: CallbackQuery):
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
      await callback.message.answer_photo(photo=photo, caption='Посморим-ка на окрестности... Куда отправимся?', reply_markup=builder.as_markup())
   else:
      await callback.message.edit_caption(caption='В окрестностях ничего нет', reply_markup=builder.as_markup())

router.include_routers(map_main.router, map_environs.router)