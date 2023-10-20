import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command
import config

# from time import sleep
import sqlite3

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.TOKEN)
# Диспетчер
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


# Создание базы данных
@dp.message(Command('bd'))
async def cmd_start(message: Message):
   firstSeen(message.chat.id)
   await message.answer('Пользователь добавлен в БД')


# Очистка базы данных
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
   await message.answer(f'Данные о пользователе: \n {message}')


# Запуск процесса поллинга новых апдейтов
async def main():
   await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())