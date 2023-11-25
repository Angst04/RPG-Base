import asyncio
import logging
from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.filters.command import Command
# from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers import main_menu, ac_desc
from storylines import test_storie
from core.keyboards import kb_menu
import config

import sqlite3

# логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()


# ********************** #
# функции для создания баз данных
def create_users_map():
   conn = sqlite3.connect('Base/data/users_map.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('''CREATE TABLE IF NOT EXISTS users_map (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               id_tg INTEGER,
               now_location TEXT DEFAULT Эвертон,
               Copper INTEGER DEFAULT 0,
               Emberwood INTEGER DEFAULT 0
               )''')
   conn.commit()

   cur.close()
   conn.close()

def create_users():
   conn = sqlite3.connect('Base/data/users.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('''CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               id_tg INTEGER,
               speed INTEGER DEFAULT 5
               )''')
   conn.commit()

   cur.close()
   conn.close()

def create_transition_events():
   conn = sqlite3.connect('Base/data/transition_events.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('''CREATE TABLE IF NOT EXISTS transition_events (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               id_tg INTEGER,
               Западня INTEGER DEFAULT 0,
               Чертополох INTEGER DEFAULT 0
               )''')
   conn.commit()

   cur.close()
   conn.close()

def create_achievements():
   conn = sqlite3.connect('Base/data/achievements.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('''CREATE TABLE IF NOT EXISTS achievements (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               id_tg INTEGER,
               a1 INTEGER,
               a2 INTEGER
               )''')
   conn.commit()

   cur.close()
   conn.close()

def firstSeen(get_id, name):
   conn = sqlite3.connect(f'Base/data/{name}.sql', check_same_thread=False)
   cur = conn.cursor()
   cur.execute(f'SELECT id_tg FROM {name} WHERE id_tg=?', (get_id,))
   rez = cur.fetchall()
   cur.close()
   conn.close()

   if not rez:
      addUser(get_id, name)
      return True
   else:
      return False

def addUser(user_id, name):
   conn = sqlite3.connect(f'Base/data/{name}.sql', check_same_thread=False)
   cur = conn.cursor()
   cur.execute(f'INSERT INTO {name} (id_tg) VALUES (?)', (user_id,))
   conn.commit()
   cur.close()
   conn.close()
# ********************** #


@dp.message(Command('start'))
async def cmd_start(message: Message):
   await message.answer('Бот работает')


# главное меню
menu_message_ids = {} # нужно перенести в бд !
@dp.message(Command('menu'))
async def cmd_menu(message: Message):
   chat_id = message.chat.id
   media = FSInputFile('Base/data/images/black.png')

   if chat_id in menu_message_ids:
      previous_menu_message_id = menu_message_ids[chat_id]
      try:
         await message.bot.delete_message(chat_id, previous_menu_message_id)
      except TelegramBadRequest:
         pass
      finally:
         await message.bot.delete_message(chat_id, previous_menu_message_id - 1)

   #menu_message = await message.answer_photo(caption='Вы находитесь в меню', reply_markup=kb_menu, photo=media)
   menu_message = await message.answer(reply_markup=kb_menu, text='Вы находитесь в меню')
   menu_message_ids[chat_id] = menu_message.message_id

   await message.bot.pin_chat_message(chat_id, menu_message.message_id)

@dp.callback_query(F.data == 'menu')
async def cbd_menu(callback: CallbackQuery):
   try:
      await callback.message.delete()
   except TelegramBadRequest:
      pass
   menu_message = await callback.message.answer(text='Вы находитесь в меню', reply_markup=kb_menu)
   menu_message_ids[callback.message.chat.id] = menu_message.message_id

   await callback.message.bot.pin_chat_message(callback.message.chat.id, menu_message.message_id)


# создание базы данных
@dp.message(Command('bd'))
async def cmd_start(message: Message):
   create_achievements()
   create_users()
   create_users_map()
   create_transition_events()

   firstSeen(message.chat.id, 'achievements')
   firstSeen(message.chat.id, 'users_map')
   firstSeen(message.chat.id, 'users')
   firstSeen(message.chat.id, 'transition_events')

   await message.answer('Пользователь добавлен в БД')


# данные пользователя
@dp.message(Command('data'))
async def cmd_data(message: Message):
   await message.answer(f'Данные о пользователе: \n{message}')


@dp.callback_query(F.data == '#')
async def f(callback: CallbackQuery):
   await callback.answer('ТЫК')


# запуск процесса поллинга новых апдейтов
async def main():
   dp.include_routers(main_menu.router, test_storie.router, ac_desc.router)

   # ответ на сообщения, отправленные до включения бота
   # await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())



"""
Архив
# Очистка БД
@dp.message(Command('clearall'))
async def cmd_start(message: Message):
   conn = sqlite3.connect('Base/data/achievements.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('DELETE FROM achievements')
   conn.commit()

   cur.close()
   conn.close()

   await message.answer('БД очищена')
   
# Удаление пользователя из БД
@dp.message(Command('clear'))
async def cmd_start(message: Message):
   conn = sqlite3.connect('Base/data/achievements.sql', check_same_thread=False)
   cur = conn.cursor()
   
   cur.execute('DELETE FROM achievements WHERE id_tg=?', (message.chat.id,))
   conn.commit()

   cur.close()
   conn.close()

   await message.answer('Пользователь удалён из БД')
"""