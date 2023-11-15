from asyncio import sleep
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from math import ceil
import sqlite3

async def transition(callback, distance, name):  
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Отменить путешествие', callback_data='map'))

   conn = sqlite3.connect('Base/data/users.sql', check_same_thread=False)

   speed = conn.execute(f'SELECT speed FROM users WHERE id_tg = {callback.message.chat.id}').fetchone()[0]
   time = distance / speed * 60

   if time < 60:
      text = 'Время в пути меньше минуты'
   elif 60 <= time < 120:
      text = 'Время в пути около минуты'
   else:
      text = f'Время в пути около {ceil(time / 60)} минут'

   await callback.message.edit_text(text=f'Вы направляетесь в {name}. {text}', reply_markup=builder.as_markup())
   await sleep(time)