from aiogram import Router
from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.dbs_config import host, user, password, db_name

from handlers.town.towns_list.everton import everton_quests

router = Router()

async def cbd_town(callback):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT now_location FROM users_map WHERE id_tg = %s', [callback.message.chat.id])
   now_location = cur.fetchone()[0]
   cur.close()
   conn.close()
   
   if now_location == 'Эвертон':
      builder = InlineKeyboardBuilder()
      builder.row(InlineKeyboardButton(text='☑️ Ратуша ☑️', callback_data='everton_quests'))
      builder.row(InlineKeyboardButton(text='Рынок', callback_data='#'))
   
      text = 'Перед вами возвышаются стены прекрасного Эвертона'
      
   builder.row(InlineKeyboardButton(text='Главное меню', callback_data='menu'))
   await callback.message.edit_text(text=text, reply_markup=builder.as_markup())

router.include_routers(everton_quests.router)