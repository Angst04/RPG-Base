import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command

from core.keyboards import main_menu
import config

import sqlite3

# логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()


# ********************** #
# Функции для создания баз данных
def create_achievements():
   conn = sqlite3.connect('data/achievements.sql', check_same_thread=False)
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
create_achievements()

def firstSeen(get_id):
   conn = sqlite3.connect('data/achievements.sql', check_same_thread=False)
   cur = conn.cursor()
   cur.execute("SELECT id_tg FROM achievements WHERE id_tg=?", (get_id,))
   rez = cur.fetchall()
   cur.close()
   conn.close()

   if not rez:
      addUser(get_id)
      return True
   else:
      return False

def addUser(user_id):
   conn = sqlite3.connect('data/achievements.sql', check_same_thread=False)
   cur = conn.cursor()
   cur.execute('INSERT INTO achievements (id_tg) VALUES (?)', (user_id,))
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

   if chat_id in menu_message_ids:
      previous_menu_message_id = menu_message_ids[chat_id]
      await message.bot.delete_message(chat_id, previous_menu_message_id)
      await message.bot.delete_message(chat_id, previous_menu_message_id - 1)

   menu_message = await message.answer(reply_markup=main_menu, text='Вы находитесь в меню')

   menu_message_ids[chat_id] = menu_message.message_id

   await message.bot.pin_chat_message(chat_id, menu_message.message_id)


# Создание базы данных
@dp.message(Command('bd'))
async def cmd_start(message: Message):
   firstSeen(message.chat.id)
   await message.answer('Пользователь добавлен в БД')


# Очистка БД
@dp.message(Command('clearall'))
async def cmd_start(message: Message):
   conn = sqlite3.connect('data/achievements.sql', check_same_thread=False)
   cur = conn.cursor()

   cur.execute('DELETE FROM achievements')
   conn.commit()

   cur.close()
   conn.close()

   await message.answer('БД очищена')
   
# Удаление пользователя из БД
@dp.message(Command('clear'))
async def cmd_start(message: Message):
   conn = sqlite3.connect('data/achievements.sql', check_same_thread=False)
   cur = conn.cursor()
   
   cur.execute('DELETE FROM achievements WHERE id_tg=?', (message.chat.id,))
   conn.commit()

   cur.close()
   conn.close()

   await message.answer('Пользователь удалён из БД')


# данные пользователя
@dp.message(Command('data'))
async def cmd_data(message: Message):
   await message.answer(f'Данные о пользователе: \n{message}')


# Запуск процесса поллинга новых апдейтов
async def main():
   await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())


# временный архив
'''
Старая реализация меню. При количетсве пользователей больше 1 будет путаться и удалять не те сообщения
menu_message_id = None
@dp.message(Command('menu'))
async def cmd_menu(message: Message, bot: Bot):
   global menu_message_id
   
   if menu_message_id:
      await bot.delete_message(chat_id=message.chat.id, message_id=menu_message_id)
      await bot.delete_message(chat_id=message.chat.id, message_id=menu_message_id - 1) # удаляет команду пользователя
   
   menu_message = await message.answer(reply_markup=main_menu, text='Вы находитесь в меню')
   menu_message_id = menu_message.message_id
   await bot.pin_chat_message(menu_message_id)
'''