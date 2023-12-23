import asyncio
import logging
from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters.command import Command


from handlers import main_menu, ac_desc, webapp
from storylines import test_storie
from core.keyboards import kb_menu, kb_menu_other
import core.databases as db
import config


# логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: Message):
   kb = [
      [KeyboardButton(text="Mini App", web_app=WebAppInfo(url='https://bespoke-boba-ec8951.netlify.app'))],
      [KeyboardButton(text="Сервер на ngrok", web_app=WebAppInfo(url='https://f66f-2a00-1370-817a-51ff-9126-863b-ed58-153c.ngrok-free.app'))] # не статическая ссылка (ngrok)
   ]
   keyboard = ReplyKeyboardMarkup(keyboard=kb)
   await message.answer("Бот работает", reply_markup=keyboard)

# главное меню
menu_message_ids = {} # нужно перенести в бд !
@dp.message(Command('menu'))
async def cmd_menu(message: Message):
   chat_id = message.chat.id
   # media = FSInputFile('Base/data/images/black.png')

   if chat_id in menu_message_ids:
      previous_menu_message_id = menu_message_ids[chat_id]
      try:
         await message.bot.delete_message(chat_id, previous_menu_message_id)
         await message.bot.delete_message(chat_id, previous_menu_message_id - 1)
      except TelegramBadRequest:
         await message.bot.delete_message(chat_id, previous_menu_message_id)

   menu_message = await message.answer(reply_markup=kb_menu, text='Вы находитесь в меню')
   menu_message_ids[chat_id] = menu_message.message_id

   await message.bot.pin_chat_message(chat_id, menu_message.message_id)

@dp.callback_query(F.data == 'menu')
async def cbd_menu(callback: CallbackQuery):
   need_pin = True
   try:
      menu_message = await callback.message.edit_text(text='Вы находитесь в меню', reply_markup=kb_menu)
      need_pin = False
   except TelegramBadRequest:
      try:
         await callback.message.delete()
      except TelegramBadRequest:
         pass
      menu_message = await callback.message.answer(text='Вы находитесь в меню', reply_markup=kb_menu)
   menu_message_ids[callback.message.chat.id] = menu_message.message_id

   if need_pin:
      await callback.message.bot.pin_chat_message(callback.message.chat.id, menu_message.message_id)


@dp.callback_query(F.data == 'menu_other')
async def cbd_menu_other(callback: CallbackQuery):
   await callback.message.edit_text(text='Вы находитесь в меню', reply_markup=kb_menu_other)

# создание базы данных
@dp.message(Command('bd'))
async def cmd_start(message: Message):
   db.start()

   db.firstSeen(message.chat.id, 'achievements')
   db.firstSeen(message.chat.id, 'users_map')
   db.firstSeen(message.chat.id, 'users')
   db.firstSeen(message.chat.id, 'transition_events')

   await message.answer('Пользователь добавлен в БД')

@dp.message(Command('drop'))
async def cmd_start(message: Message):
   db.drop()
   await message.answer('Базы данных удалены')

# данные пользователя
@dp.message(Command('data'))
async def cmd_data(message: Message):
   await message.answer(f'Данные о пользователе: \n{message}')

@dp.callback_query(F.data == '#')
async def f(callback: CallbackQuery):
   await callback.answer('ТЫК')


async def main():
   dp.include_routers(main_menu.router, test_storie.router, ac_desc.router, webapp.router)

   # ответ на сообщения, отправленные до включения бота
   # await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())



"""
Архив

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
               last_event INTEGER DEFAULT 0,
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
               a1 INTEGER DEFAULT 0,
               a2 INTEGER DEFAULT 0
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