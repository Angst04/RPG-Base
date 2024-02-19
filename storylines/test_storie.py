from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from time import sleep

router = Router()

@router.callback_query(F.data == 'test_msg_1')
async def test_msg_1(callback: CallbackQuery):
   await callback.message.answer(text='Добро пожаловать в тестовую историю')
   sleep(1)

   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='*Далее*', callback_data='#'))
   await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

   builder = InlineKeyboardBuilder()
   builder.add(InlineKeyboardButton(text='Далее', callback_data='test_msg_2'))
   await callback.message.answer('Этап 1', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'test_msg_2')
async def test_msg_2(callback: CallbackQuery):
   await callback.message.edit_reply_markup()

   builder = InlineKeyboardBuilder()
   builder.adjust(2)
   builder.add(InlineKeyboardButton(text='Налево', callback_data='test_msg_3'))
   builder.add(InlineKeyboardButton(text='Направо', callback_data='test_msg_4'))
   await callback.message.answer(text='Куда пойдём?', reply_markup=builder.as_markup())

@router.callback_query(F.data == 'test_msg_3')
async def test_msg_2(callback: CallbackQuery):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   cur.execute(f'SELECT a1 FROM achievements WHERE id_tg = %s', [callback.message.chat.id])
   if cur.fetchone() != 1:
      await callback.answer(text='Получено достижение!', show_alert=True)

   cur.execute(f'UPDATE achievements SET a1 = 1 WHERE id_tg=%s', [callback.message.chat.id])

   conn.commit()
   cur.close()
   conn.close()

   await callback.message.answer(text='Вы в саду')

@router.callback_query(F.data == 'test_msg_4')
async def test_msg_2(callback: CallbackQuery):
   await callback.answer(text='Ждём...')
   sleep(1)
   await callback.answer(text='Вы в лесу', show_alert=True)