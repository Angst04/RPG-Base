from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

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

   cur.execute(f'UPDATE transition_events SET Чертополох = 1 WHERE id_tg= %s', [callback.message.chat.id])
   conn.commit()
   cur.close()
   conn.close()
   
   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Далее', callback_data='msg1'))

   await callback.message.answer(text='Что-то пошло не так...', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'msg1')
async def f(callback: CallbackQuery):
   await callback.message.edit_reply_markup()

   builder = InlineKeyboardBuilder()
   builder.row(InlineKeyboardButton(text='Выбраться из ловушки', callback_data='menu'))

   sleep(1)
   await callback.message.answer(text='Нужно выбираться отсюда', reply_markup=builder.as_markup())