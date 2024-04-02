from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

from time import sleep

router = Router()

async def start(callback):
   await callback.message.delete()

   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   cur.execute(f'UPDATE transition_events SET Западня = 1 WHERE id_tg= %s', [callback.message.chat.id])
   conn.commit()
   cur.close()
   conn.close()
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Далее', callback_data='msg1'))

   await callback.message.answer(text='Кажется я слышу шорох в кустах...', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'msg1')
async def f(callback: CallbackQuery):
   await callback.message.edit_reply_markup()

   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Выбраться из тоннеля', callback_data='menu'))

   await callback.message.answer(text='Нет, точно слышу')
   sleep(1)
   await callback.message.answer(text='Кажется кто-то следит за мной', reply_markup=builder.as_markup())