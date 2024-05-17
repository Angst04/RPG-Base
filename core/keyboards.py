from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name


enemy_loc = ['лесопилка Доппи', 'Амбербрук', 'Эвертон']
town_loc = ['Эвертон']

def kb_menu(chat_id):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT now_location FROM users_map WHERE id_tg = %s', [chat_id])
   now_location = cur.fetchone()[0]
   cur.close()
   conn.close()
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Карта', callback_data='map'))
   if now_location in town_loc:
      builder.row(InlineKeyboardButton(text='Город', callback_data='town'))
   if now_location in enemy_loc:
      builder.row(InlineKeyboardButton(text='Поиск противника', callback_data='find_enemy'))
   builder.row(InlineKeyboardButton(text='Мои поручения', callback_data='my_quests'))
   builder.row(InlineKeyboardButton(text='Инвентарь', web_app=WebAppInfo(url='https://c4be-2a00-1370-817a-4eea-80f9-4b5a-b8a8-9cb.ngrok-free.app')))
   builder.row(InlineKeyboardButton(text='Дополнительно', callback_data='menu_other'))
   
   return builder.as_markup()

kb_menu_other = InlineKeyboardMarkup(inline_keyboard=[
   [
      InlineKeyboardButton(
         text='Тестовый старт',
         callback_data='test_msg_1'
      )
   ],
   [
      InlineKeyboardButton(
         text='Персонаж',
         callback_data='hero'
      )
   ],
   [
      InlineKeyboardButton(
         text='Достижения',
         callback_data='achievements'
      )
   ],
   [
      InlineKeyboardButton(
         text='Фрагменты',
         callback_data='fragments'
      )
   ],
   [
      InlineKeyboardButton(
         text='Главное меню',
         callback_data='menu'
      )
   ]
])