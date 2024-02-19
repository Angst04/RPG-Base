from asyncio import sleep
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from core.health_ind import health_ind

router = Router()

async def battle_prepare(callback, text, photo, amount):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT health FROM users WHERE id_tg = %s', [callback.message.chat.id])
   player_hp = cur.fetchone()[0]
   
   # противник
   cur.execute(f'UPDATE users SET enemy_health = %s WHERE id_tg=%s', [amount, callback.message.chat.id])
   conn.commit()
   cur.close()
   conn.close()

   builder = InlineKeyboardBuilder()
   await health_ind(amount=amount, builder=builder)
   
   await callback.message.delete()
   await sleep(0.75)
   await callback.message.answer_photo(photo=photo, caption=text, reply_markup=builder.as_markup())
   
   # игрок
   builder_2 = InlineKeyboardBuilder()
   await health_ind(amount=player_hp, builder=builder_2)
   
   builder_2.row(InlineKeyboardButton(text='Выбрать карту', callback_data='test_attack'))
   
   await sleep(0.75)
   await callback.message.answer(text='Информация о вашем герое', reply_markup=builder_2.as_markup())
   
   
async def edit_health(callback, amount):
   builder = InlineKeyboardBuilder()
   await health_ind(amount=amount, builder=builder)
   
   await callback.message.edit_text(text='', inline_message_id=str(callback.message.message_id - 1), reply_markup=builder.as_markup())

   
@router.callback_query(F.data == 'test_attack')
async def f(callback: CallbackQuery):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT enemy_health FROM users WHERE id_tg = %s', [callback.message.chat.id])
   enemy_health = cur.fetchone()[0]
   
   enemy_health -= 5
   if enemy_health <= 0:
      builder = InlineKeyboardBuilder()
      builder.row(InlineKeyboardButton(text='Вернуться в меню', callback_data='menu'))
      
      cur.execute(f'UPDATE users SET enemy_health = 0 WHERE id_tg=%s', [callback.message.chat.id])
      conn.commit()
      
      await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
      await sleep(0.75)
      await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
      await sleep(0.75)
      await callback.message.answer(text='Враг повержен', reply_markup=builder.as_markup())
   else:
      cur.execute(f'UPDATE users SET enemy_health = %s WHERE id_tg=%s', [enemy_health, callback.message.chat.id])
      conn.commit()
      
      await edit_health(callback=callback, amount=enemy_health)
         
   cur.close()
   conn.close()