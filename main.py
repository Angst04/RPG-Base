import asyncio
from asyncio import sleep
import logging
from aiogram.exceptions import TelegramBadRequest
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


from handlers import main_menu, webapp
from storylines import test_storie
from core.keyboards import kb_menu, kb_menu_other
import core.databases as db
from apps.battle import battle_main
import config

import psycopg2
from core.dbs_config import host, user, password, db_name

# логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher()


class RegisterMessages(StatesGroup):
   name = State()

@dp.message(StateFilter(None), Command("start"))
async def cmd_menu(message: Message, state: FSMContext):
   conn = psycopg2.connect(
         host=host,
         user=user,
         password=password,
         database=db_name
      )
   cur = conn.cursor()
   
   cur.execute(f'SELECT name FROM users WHERE id_tg=%s', [message.chat.id])
   if cur.fetchone()[0] != None:
      await message.answer('Вы уже проходили регистрацию. Изменить имя можно в другом месте')
      # await sleep(5)
      # await message.bot.delete_messages(message.chat.id, [message.message_id + 1, message.message_id])

   else:
      await message.answer('Привет странник! Как тебя зовут?')
      await state.set_state(RegisterMessages.name)
   
@dp.message(F.text, RegisterMessages.name)
async def reg_step1(message: Message, state: FSMContext):
   # нужно написать фильтр на имена
   if message.text == 'Justifall':
      conn = psycopg2.connect(
         host=host,
         user=user,
         password=password,
         database=db_name
      )
      cur = conn.cursor()
      cur.execute(f'UPDATE users SET name = %s WHERE id_tg=%s', [message.text, message.chat.id])
      conn.commit()
      cur.close()
      conn.close()
      
      await message.answer('Так и запишем...')
      await state.clear()
      await sleep(1.5)
      
      builder = InlineKeyboardBuilder()
      builder.row(InlineKeyboardButton(text='Перейти в меню', callback_data='menu'))
      
      await message.answer(text='Теперь вы готовы отправиться в грандиозное приключение!', reply_markup=builder.as_markup())
      await sleep(1.5)
      await message.bot.delete_messages(message.chat.id, [message.message_id + 1, message.message_id, message.message_id - 1, message.message_id - 2])
   else:
      await message.answer('Это имя занято, введите другое')

# главное меню
menu_message_ids = {} # нужно перенести в бд !
@dp.message(Command('menu'))
async def cmd_menu(message: Message):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT busy FROM users WHERE id_tg=%s', [message.chat.id])
   if cur.fetchone()[0] == 1:
      # должно всплывать "не сейчас"
      return
   
   chat_id = message.chat.id

   if chat_id in menu_message_ids:
      prev_menu_id = menu_message_ids[chat_id]
      try:
         await message.bot.delete_messages(chat_id, [prev_menu_id, prev_menu_id - 1])
         await sleep(0.75)
      except TelegramBadRequest:
         pass

   menu_message = await message.answer(reply_markup=kb_menu(chat_id), text='Вы находитесь в меню')
   menu_message_ids[chat_id] = menu_message.message_id

   # await sleep(1)
   # await message.bot.pin_chat_message(chat_id, menu_message.message_id)

@dp.callback_query(F.data == 'menu')
async def cbd_menu(callback: CallbackQuery):
   chat_id = callback.message.chat.id
   # need_pin = True
   try:
      menu_message = await callback.message.edit_text(text='Вы находитесь в меню', reply_markup=kb_menu(chat_id))
      # need_pin = False
   except TelegramBadRequest:
      try:
         await callback.message.delete()
      except TelegramBadRequest:
         pass
      await sleep(0.75)
      menu_message = await callback.message.answer(text='Вы находитесь в меню', reply_markup=kb_menu(chat_id))
   menu_message_ids[callback.message.chat.id] = menu_message.message_id

   # if need_pin:
   #    await sleep(1)
   #    await callback.message.bot.pin_chat_message(callback.message.chat.id, menu_message.message_id)


@dp.callback_query(F.data == 'menu_other')
async def cbd_menu_other(callback: CallbackQuery):
   await callback.message.edit_text(text='Вы находитесь в дополнительном меню', reply_markup=kb_menu_other)

# создание базы данных
@dp.message(Command('db'))
async def cmd_db(message: Message):
   db.start()   

   # при первом добавлении таблицы не вписывать сюда
   db.firstSeen(message.chat.id, 'users')
   db.firstSeen(message.chat.id, 'users_map')
   db.firstSeen(message.chat.id, 'transition_events')
   db.firstSeen(message.chat.id, 'achievements')
   db.firstSeen(message.chat.id, 'collections')
   db.firstSeen(message.chat.id, 'inventories')
   db.firstSeen(message.chat.id, 'quests')
   db.firstSeen(message.chat.id, 'fragments')
   
   await message.answer('Пользователь добавлен в БД')

@dp.message(Command('drop'))
async def cmd_drop(message: Message):
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
   dp.include_routers(main_menu.router, test_storie.router, webapp.router, battle_main.router)

   # ответ на сообщения, отправленные до включения бота
   # await bot.delete_webhook(drop_pending_updates=True)
   await dp.start_polling(bot)

if __name__ == "__main__":
   asyncio.run(main())