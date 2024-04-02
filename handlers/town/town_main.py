from aiogram import Router
from aiogram.types import InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

from handlers.town import town_quests

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
   
   builder = InlineKeyboardBuilder()
   
   if now_location == 'Эвертон':
      text = 'Перед вами возвышаются стены прекрасного Эвертона'
      name_quests = '☑️ Ратуша ☑️'
      name_market = 'Рынок'
   
   elif now_location == 'имение Чапси':
      text = 'Вы стоите посреди деревеньки с затхлым запахом'
      name_quests = '☑️ Доска поручений ☑️'
      name_market = 'Изба барахольщиков'
   
   builder.row(InlineKeyboardButton(text=name_quests, callback_data='quests'))
   builder.row(InlineKeyboardButton(text=name_market, callback_data='market'))
   builder.row(InlineKeyboardButton(text='Главное меню', callback_data='menu'))
   await callback.message.edit_text(text=text, reply_markup=builder.as_markup())
   
router.include_routers(town_quests.router)