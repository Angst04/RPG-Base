from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery,ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.map import map_main, map_environs

from core.keyboards import kb_menu
import sqlite3

router = Router()

@router.callback_query(F.data == 'achievements')
async def cbd_achievements(callback: CallbackQuery):
   conn = sqlite3.connect('Base/data/achievements.sql', check_same_thread=False)

   builder = InlineKeyboardBuilder()
   k = 0

   if conn.execute(f'SELECT a1 FROM achievements WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 1:
      builder.row(InlineKeyboardButton(text='Серьёзный выбор', callback_data='AC1'))
      k += 1
   if conn.execute(f'SELECT a2 FROM achievements WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 1:
      builder.row(InlineKeyboardButton('Не менее серьёзный выбор', callback_data='AC2'))
      k += 1

   builder.row(InlineKeyboardButton(text='Назад', callback_data='menu'))
   if k > 0:
      await callback.message.edit_text(text='Ваши достижения', reply_markup=builder.as_markup())
   elif k == 0:
      await callback.message.edit_text(text='Здесь ничего нет(', reply_markup=builder.as_markup())

   conn.close()


@router.callback_query(F.data == 'map')
async def cbd_map(callback: CallbackQuery):
   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)

   builder = InlineKeyboardBuilder()
   
   now_location = conn.execute(f'SELECT now_location FROM users_map WHERE id_tg = {callback.message.chat.id}').fetchone()[0]

   builder.row(InlineKeyboardButton(text=f'{now_location.title()} <- вы здесь', callback_data='#'))

   if now_location == 'Эвертон':
      builder.row(InlineKeyboardButton(text='Имение Чапси', callback_data='имение Чапси'))
      builder.row(InlineKeyboardButton(text='Амбербрук', callback_data='Амбербрук'))
   if now_location == 'Амбербрук':
      builder.row(InlineKeyboardButton(text='Эвертон', callback_data='Эвертон'))
      if conn.execute(f'SELECT Copper FROM users_map WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 1:
         builder.row(InlineKeyboardButton(text='Коппер', callback_data='Коппер'))
   if now_location == 'имение Чапси':
      builder.row(InlineKeyboardButton(text='Эвертон', callback_data='Эвертон'))
      if conn.execute(f'SELECT Emberwood FROM users_map WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 1:
         builder.row(InlineKeyboardButton(text='Эмбервуд', callback_data='Эмбервуд'))
   
   builder.row(InlineKeyboardButton(text='Окрестности', callback_data='environs'))

   await callback.message.edit_text(text='Вы открываете карту. Куда отправимся?', reply_markup=builder.as_markup())

   conn.close()

@router.callback_query(F.data == 'environs')
async def f(callback: CallbackQuery):
   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   builder = InlineKeyboardBuilder()
   now_location = conn.execute(f'SELECT now_location FROM users_map WHERE id_tg = {callback.message.chat.id}').fetchone()[0]
   flag = False

   if now_location == 'Эвертон':
      flag = True
      builder.row(InlineKeyboardButton(text='Лесопилка Доппи', callback_data='Лесопилка Доппи'))
   
   builder.row(InlineKeyboardButton(text='Назад', callback_data='map'))

   if flag:
      await callback.message.edit_text(text='Вы открываете карту. Куда отправимся?', reply_markup=builder.as_markup())
   else:
      await callback.message.edit_text(text='В окрестностях ничего нет', reply_markup=builder.as_markup())

router.include_routers(map_main.router, map_environs.router)