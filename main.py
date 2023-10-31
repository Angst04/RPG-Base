import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
# Функции для создания баз данных
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
create_achievements()

def firstSeen(get_id):
   conn = sqlite3.connect('Base/data/achievements.sql', check_same_thread=False)
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
   conn = sqlite3.connect('Base/data/achievements.sql', check_same_thread=False)
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

   menu_message = await message.answer(reply_markup=kb_menu, text='Вы находитесь в меню')

   menu_message_ids[chat_id] = menu_message.message_id

   await message.bot.pin_chat_message(chat_id, menu_message.message_id)

@dp.callback_query(F.data == 'menu')
async def cbd_menu(callback: CallbackQuery):
   await callback.message.edit_text(text='Вы находитесь в меню', reply_markup=kb_menu)


# тестовая история (надо переместить в меню)
@dp.message(Command('storie'))
async def cmd_storie(message: Message):
   btn_text='Далее'
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(
      text=btn_text, callback_data='test_msg_1'
   ))
   
   await message.answer(text='Добро пожаловать в тестовую историю', reply_markup=builder.as_markup())


# Создание базы данных
@dp.message(Command('bd'))
async def cmd_start(message: Message):
   firstSeen(message.chat.id)
   await message.answer('Пользователь добавлен в БД')


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


# данные пользователя
@dp.message(Command('data'))
async def cmd_data(message: Message):
   await message.answer(f'Данные о пользователе: \n{message}')


# Запуск процесса поллинга новых апдейтов
async def main():
   dp.include_routers(main_menu.router, test_storie.router, ac_desc.router)

   # ответ на сообщения, отправленные до включения бота
   # await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())